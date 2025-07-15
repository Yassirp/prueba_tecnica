from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse
from datetime import datetime
import pytz
from typing import Optional
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from fastapi import HTTPException

class ReportService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def generate_users_report(self, format: str = "excel", filters: dict = None) -> StreamingResponse:
        """Genera un reporte de usuarios en Excel o PDF según el parámetro 'format' y aplica filtros opcionales"""
        filters = filters or {}
        where_clauses = ["u.deleted_at IS NULL"]
        params = {}
        if filters.get("role_id") is not None:
            where_clauses.append("u.role_id = :role_id")
            params["role_id"] = filters["role_id"]
        if filters.get("department_id") is not None:
            where_clauses.append("u.department_id = :department_id")
            params["department_id"] = filters["department_id"]
        if filters.get("municipality_id") is not None:
            where_clauses.append("u.municipality_id = :municipality_id")
            params["municipality_id"] = filters["municipality_id"]
        if filters.get("country_id") is not None:
            where_clauses.append("u.country_id = :country_id")
            params["country_id"] = filters["country_id"]
        if filters.get("is_active") is not None:
            where_clauses.append("u.is_active = :is_active")
            params["is_active"] = filters["is_active"]
        if filters.get("state") is not None:
            where_clauses.append("u.state = :state")
            params["state"] = filters["state"]
        if filters.get("created_at_from"):
            where_clauses.append("u.created_at >= :created_at_from")
            params["created_at_from"] = filters["created_at_from"]
        if filters.get("created_at_to"):
            where_clauses.append("u.created_at <= :created_at_to")
            params["created_at_to"] = filters["created_at_to"]
        where_sql = " AND ".join(where_clauses)
        users_query = text(f"""
            SELECT 
                CONCAT(u.name, ' ', u.last_name) as nombre_completo,
                u.email as correo_electronico,
                pv.value as tipo_documento,
                u.document_number as numero_documento,
                u.phone as telefono,
                u.address as direccion,
                u.is_active as estado,
                c.name as pais,
                d.name as departamento,
                m.name as municipio,
                r.name as rol,
                u.created_at as fecha_creacion
            FROM m_users u
            LEFT JOIN countries c ON u.country_id = c.id
            LEFT JOIN departments d ON u.department_id = d.id
            LEFT JOIN municipalities m ON u.municipality_id = m.id
            LEFT JOIN m_roles r ON u.role_id = r.id
            LEFT JOIN m_parameters_values pv ON u.document_type = pv.id
            WHERE {where_sql}
            ORDER BY u.id
        """)
        relationships_query = text("""
            SELECT 
                ur.id,
                u1.name || ' ' || u1.last_name as usuario_nombre,
                u2.name || ' ' || u2.last_name as relacionado_nombre,
                pv.value as tipo_relacion,
                os.name as estado_relacion,
                ur.created_at as fecha_creacion
            FROM c_user_relationship ur
            JOIN m_users u1 ON ur.user_id = u1.id
            JOIN m_users u2 ON ur.user_relationship_id = u2.id
            JOIN m_parameters_values pv ON ur.relationship_type_id = pv.id
            JOIN m_object_states os ON ur.relationship_status_id = os.id
            WHERE ur.deleted_at IS NULL
            ORDER BY ur.id
        """)
        stats_query = text("""
            SELECT 
                COUNT(*) as total_usuarios,
                COUNT(CASE WHEN u.is_active = true THEN 1 END) as usuarios_activos,
                COUNT(CASE WHEN u.state = 1 THEN 1 END) as usuarios_aprobados,
                COUNT(CASE WHEN u.state = 2 THEN 1 END) as usuarios_pendientes,
                COUNT(DISTINCT u.country_id) as total_paises,
                COUNT(DISTINCT u.department_id) as total_departamentos,
                COUNT(DISTINCT u.role_id) as total_roles
            FROM m_users u
            WHERE u.deleted_at IS NULL
        """)
        
        # Ejecutar consultas
        users_result = await self.db_session.execute(users_query, params)
        relationships_result = await self.db_session.execute(relationships_query)
        stats_result = await self.db_session.execute(stats_query)
        
        # Convertir resultados a DataFrames
        users_df = pd.DataFrame(users_result.fetchall(), columns=pd.Index(users_result.keys()))
        relationships_df = pd.DataFrame(relationships_result.fetchall(), columns=pd.Index(relationships_result.keys()))
        stats_df = pd.DataFrame(stats_result.fetchall(), columns=pd.Index(stats_result.keys()))
        
        # Convertir fechas con timezone a timezone-naive para Excel/PDF
        if not users_df.empty:
            for col in ['fecha_creacion', 'fecha_actualizacion']:
                if col in users_df.columns:
                    users_df[col] = pd.to_datetime(users_df[col]).dt.tz_localize(None)
        if not relationships_df.empty:
            if 'fecha_creacion' in relationships_df.columns:
                relationships_df['fecha_creacion'] = pd.to_datetime(relationships_df['fecha_creacion']).dt.tz_localize(None)
        
        # Resúmenes
        country_summary = users_df.groupby('pais').agg({
            'nombre_completo': 'count',
            'estado': lambda x: (x == True).sum()
        }) if not users_df.empty else pd.DataFrame()
        if not country_summary.empty:
            country_summary.columns = ['Total Usuarios', 'Usuarios Activos']
        role_summary = users_df.groupby('rol').agg({
            'nombre_completo': 'count',
            'estado': lambda x: (x == True).sum()
        }) if not users_df.empty else pd.DataFrame()
        if not role_summary.empty:
            role_summary.columns = ['Total Usuarios', 'Usuarios Activos']
        
        if format == "pdf":
            # Eliminar columnas no deseadas para el PDF
            cols_ocultar = ["estado", "creado_por", "fecha_actualizacion", "rol", "pais"]
            users_df_pdf = users_df.drop(columns=[col for col in cols_ocultar if col in users_df.columns])

            output = BytesIO()
            doc = SimpleDocTemplate(output, pagesize=landscape(letter))
            elements = []
            styles = getSampleStyleSheet()
            # Usuarios
            elements.append(Paragraph("Usuarios", styles['Heading1']))
            if not users_df_pdf.empty:
                data = [users_df_pdf.columns.tolist()] + users_df_pdf.astype(str).values.tolist()
                # Ajustar anchos de columna proporcionalmente
                col_widths = [max(60, min(200, max([len(str(x)) for x in [col] + users_df_pdf[col].astype(str).tolist()]) * 5)) for col in users_df_pdf.columns]
                t = Table(data, repeatRows=1, colWidths=col_widths)
                t.setStyle(TableStyle([
                    ('FONTSIZE', (0,0), (-1,-1), 6),
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 5),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("Sin datos de usuarios", styles['Normal']))
            elements.append(PageBreak())
            # Relaciones
            elements.append(Paragraph("Relaciones de Usuarios", styles['Heading1']))
            if not relationships_df.empty:
                data = [relationships_df.columns.tolist()] + relationships_df.astype(str).values.tolist()
                t = Table(data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 8),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("Sin datos de relaciones", styles['Normal']))
            elements.append(PageBreak())
            # Estadísticas
            elements.append(Paragraph("Estadísticas", styles['Heading1']))
            if not stats_df.empty:
                data = [stats_df.columns.tolist()] + stats_df.astype(str).values.tolist()
                t = Table(data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 8),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("Sin datos de estadísticas", styles['Normal']))
            elements.append(PageBreak())
            # Resumen por País
            elements.append(Paragraph("Resumen por País", styles['Heading1']))
            if not country_summary.empty:
                data = [list(country_summary.columns)] + country_summary.reset_index().astype(str).values.tolist()
                t = Table(data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 8),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("Sin datos de resumen por país", styles['Normal']))
            elements.append(PageBreak())
            # Resumen por Rol
            elements.append(Paragraph("Resumen por Rol", styles['Heading1']))
            if not role_summary.empty:
                data = [list(role_summary.columns)] + role_summary.reset_index().astype(str).values.tolist()
                t = Table(data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 8),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("Sin datos de resumen por rol", styles['Normal']))
            doc.build(elements)
            output.seek(0)
            timestamp = datetime.now(pytz.timezone('America/Bogota')).strftime('%Y%m%d_%H%M%S')
            filename = f"reporte_usuarios_{timestamp}.pdf"
            return StreamingResponse(
                output,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        else:
            # Excel (comportamiento original)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                users_df.to_excel(writer, sheet_name='Usuarios', index=False)
                relationships_df.to_excel(writer, sheet_name='Relaciones', index=False)
                stats_df.to_excel(writer, sheet_name='Estadísticas', index=False)
                if not country_summary.empty:
                    country_summary.to_excel(writer, sheet_name='Resumen por País')
                if not role_summary.empty:
                    role_summary.to_excel(writer, sheet_name='Resumen por Rol')
            output.seek(0)
            timestamp = datetime.now(pytz.timezone('America/Bogota')).strftime('%Y%m%d_%H%M%S')
            filename = f"reporte_usuarios_{timestamp}.xlsx"
            return StreamingResponse(
                output,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

    async def generate_user_relationships_report(self, user_id: Optional[int] = None, format: str = "excel") -> StreamingResponse:
        """Genera un reporte específico de relaciones de usuarios en Excel o PDF"""
        
        if not user_id:
            raise HTTPException(status_code=400, detail="el id del usuario es requerido")
        
        query = text("""
            SELECT 
                u1.name || ' ' || u1.last_name as usuario_nombre,
                u1.email as usuario_correo,
                u2.name || ' ' || u2.last_name as relacionado_nombre,
                u2.email as relacionado_correo,
                pv.value as tipo_relacion,
                os.name as estado_relacion,
                ur.created_at as fecha_creacion
            FROM c_user_relationship ur
            JOIN m_users u1 ON ur.user_id = u1.idiid
            JOIN m_object_states os ON ur.relationship_status_id = os.id
            WHERE ur.deleted_at IS NULL 
            AND (ur.user_id = :user_id OR ur.user_relationship_id = :user_id)
            ORDER BY ur.created_at DESC
        """)
        result = await self.db_session.execute(query, {"user_id": user_id})
        
        # Convertir a DataFrame
        df = pd.DataFrame(result.fetchall(), columns=pd.Index(result.keys()))
        
        # Convertir fechas con timezone a timezone-naive para Excel/PDF
        if not df.empty and 'fecha_creacion' in df.columns:
            df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion']).dt.tz_localize(None)
        
        if format == "pdf":
            output = BytesIO()
            doc = SimpleDocTemplate(output, pagesize=landscape(letter))
            elements = []
            styles = getSampleStyleSheet()
            # Tabla principal
            elements.append(Paragraph("Relaciones de Usuarios", styles['Heading1']))
            if not df.empty:
                data = [df.columns.tolist()] + df.astype(str).values.tolist()
                col_widths = [max(60, min(200, max([len(str(x)) for x in [col] + df[col].astype(str).tolist()]) * 5)) for col in df.columns]
                t = Table(data, repeatRows=1, colWidths=col_widths)
                t.setStyle(TableStyle([
                    ('FONTSIZE', (0,0), (-1,-1), 6),
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 5),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("Sin datos de relaciones", styles['Normal']))
            elements.append(PageBreak())
            # Resumen por tipo de relación
            if not df.empty and ('tipo_relacion' in df.columns):
                relationship_summary = df.groupby('tipo_relacion').size().reset_index(name='Total Relaciones')
                elements.append(Paragraph("Resumen por Tipo de Relación", styles['Heading1']))
                data = [relationship_summary.columns.tolist()] + relationship_summary.astype(str).values.tolist()
                t = Table(data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('FONTSIZE', (0,0), (-1,-1), 7),
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 6),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
                elements.append(PageBreak())
            # Resumen por estado
            if not df.empty and ('estado_relacion' in df.columns):
                status_summary = df.groupby('estado_relacion').size().reset_index(name='Total Relaciones')
                elements.append(Paragraph("Resumen por Estado de Relación", styles['Heading1']))
                data = [status_summary.columns.tolist()] + status_summary.astype(str).values.tolist()
                t = Table(data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('FONTSIZE', (0,0), (-1,-1), 7),
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 6),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(t)
            doc.build(elements)
            output.seek(0)
            timestamp = datetime.now(pytz.timezone('America/Bogota')).strftime('%Y%m%d_%H%M%S')
            filename = f"reporte_relaciones_{timestamp}.pdf"
            return StreamingResponse(
                output,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        else:
            # Excel (comportamiento original)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Relaciones de Usuarios', index=False)
                # Resumen por tipo de relación
                if not df.empty:
                    if 'tipo_relacion' in df.columns:
                        relationship_summary = df.groupby('tipo_relacion').size().reset_index(name='Total Relaciones')
                        relationship_summary.to_excel(writer, sheet_name='Resumen por Tipo', index=False)
                    if 'estado_relacion' in df.columns:
                        status_summary = df.groupby('estado_relacion').size().reset_index(name='Total Relaciones')
                        status_summary.to_excel(writer, sheet_name='Resumen por Estado', index=False)
            output.seek(0)
            timestamp = datetime.now(pytz.timezone('America/Bogota')).strftime('%Y%m%d_%H%M%S')
            filename = f"reporte_relaciones_{timestamp}.xlsx"
            return StreamingResponse(
                output,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            ) 