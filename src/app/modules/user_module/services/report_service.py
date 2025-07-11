from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse
from datetime import datetime
import pytz
from typing import Optional

class ReportService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def generate_users_excel_report(self) -> StreamingResponse:
        """Genera un reporte de Excel con datos de usuarios y sus relaciones usando consultas SQL puras"""
        
        # Consulta SQL para obtener usuarios con información completa
        users_query = text("""
            SELECT 
                CONCAT(u.name, ' ', u.last_name) as nombre_completo,
                u.email as correo_electronico,
                u.document_number as numero_documento,
                u.phone as telefono,
                u.address as direccion,
                u.is_active as estado_activo,
                u.created_at as fecha_creacion,
                u.updated_at as fecha_actualizacion,
                c.name as pais,
                d.name as departamento,
                m.name as municipio,
                r.name as rol,
                pv.value as tipo_documento,
                creator.name || ' ' || creator.last_name as creado_por
            FROM m_users u
            LEFT JOIN countries c ON u.country_id = c.id
            LEFT JOIN departments d ON u.department_id = d.id
            LEFT JOIN municipalities m ON u.municipality_id = m.id
            LEFT JOIN m_roles r ON u.role_id = r.id
            LEFT JOIN m_parameters_values pv ON u.document_type = pv.id
            LEFT JOIN m_users creator ON u.created_by = creator.id
            WHERE u.deleted_at IS NULL
            ORDER BY u.id
        """)
        
        # Consulta SQL para obtener relaciones de usuarios
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
        
        # Consulta SQL para obtener estadísticas
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
        users_result = await self.db_session.execute(users_query)
        relationships_result = await self.db_session.execute(relationships_query)
        stats_result = await self.db_session.execute(stats_query)
        
        # Convertir resultados a DataFrames
        users_df = pd.DataFrame(users_result.fetchall(), columns=pd.Index(users_result.keys()))
        relationships_df = pd.DataFrame(relationships_result.fetchall(), columns=pd.Index(relationships_result.keys()))
        stats_df = pd.DataFrame(stats_result.fetchall(), columns=pd.Index(stats_result.keys()))
        
        # Convertir fechas con timezone a timezone-naive para Excel
        if not users_df.empty:
            for col in ['fecha_creacion', 'fecha_actualizacion']:
                if col in users_df.columns:
                    users_df[col] = pd.to_datetime(users_df[col]).dt.tz_localize(None)
        
        if not relationships_df.empty:
            if 'fecha_creacion' in relationships_df.columns:
                relationships_df['fecha_creacion'] = pd.to_datetime(relationships_df['fecha_creacion']).dt.tz_localize(None)
        
        # Crear archivo Excel en memoria
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Hoja 1: Usuarios
            users_df.to_excel(writer, sheet_name='Usuarios', index=False)
            
            # Hoja 2: Relaciones de Usuarios
            relationships_df.to_excel(writer, sheet_name='Relaciones', index=False)
            
            # Hoja 3: Estadísticas
            stats_df.to_excel(writer, sheet_name='Estadísticas', index=False)
            
            # Hoja 4: Resumen por País
            country_summary = users_df.groupby('pais').agg({
                'nombre_completo': 'count',
                'estado_activo': lambda x: (x == True).sum()
            })
            country_summary.columns = ['Total Usuarios', 'Usuarios Activos']
            country_summary.to_excel(writer, sheet_name='Resumen por País')
            
            # Hoja 5: Resumen por Rol
            role_summary = users_df.groupby('rol').agg({
                'nombre_completo': 'count',
                'estado_activo': lambda x: (x == True).sum()
            })
            role_summary.columns = ['Total Usuarios', 'Usuarios Activos']
            role_summary.to_excel(writer, sheet_name='Resumen por Rol')
        
        output.seek(0)
        
        # Generar nombre del archivo con timestamp
        timestamp = datetime.now(pytz.timezone('America/Bogota')).strftime('%Y%m%d_%H%M%S')
        filename = f"reporte_usuarios_{timestamp}.xlsx"
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    async def generate_user_relationships_report(self, user_id: Optional[int] = None) -> StreamingResponse:
        """Genera un reporte específico de relaciones de usuarios"""
        
        if user_id:
            # Reporte para un usuario específico
            query = text("""
                SELECT 
                    u1.id as usuario_id,
                    u1.name || ' ' || u1.last_name as usuario_nombre,
                    u1.email as usuario_correo,
                    u2.id as relacionado_id,
                    u2.name || ' ' || u2.last_name as relacionado_nombre,
                    u2.email as relacionado_correo,
                    pv.value as tipo_relacion,
                    os.name as estado_relacion,
                    ur.created_at as fecha_creacion
                FROM c_user_relationship ur
                JOIN m_users u1 ON ur.user_id = u1.id
                JOIN m_users u2 ON ur.user_relationship_id = u2.id
                JOIN m_parameters_values pv ON ur.relationship_type_id = pv.id
                JOIN m_object_states os ON ur.relationship_status_id = os.id
                WHERE ur.deleted_at IS NULL 
                AND (ur.user_id = :user_id OR ur.user_relationship_id = :user_id)
                ORDER BY ur.created_at DESC
            """)
            result = await self.db_session.execute(query, {"user_id": user_id})
        else:
            # Reporte general de relaciones
            query = text("""
                SELECT 
                    u1.name || ' ' || u1.last_name as nombre_completo,
                    u1.email as usuario_correo,
                    u2.name || ' ' || u2.last_name as nombre_completo,
                    u2.email as relacionado_correo,
                    pv.value as tipo_relacion,
                    os.name as estado_relacion,
                    ur.created_at as fecha_creacion
                FROM c_user_relationship ur
                JOIN m_users u1 ON ur.user_id = u1.id
                JOIN m_users u2 ON ur.user_relationship_id = u2.id
                JOIN m_parameters_values pv ON ur.relationship_type_id = pv.id
                JOIN m_object_states os ON ur.relationship_status_id = os.id
                WHERE ur.deleted_at IS NULL
                ORDER BY ur.created_at DESC
            """)
            result = await self.db_session.execute(query)
        
        # Convertir a DataFrame
        df = pd.DataFrame(result.fetchall(), columns=pd.Index(result.keys()))
        
        # Convertir fechas con timezone a timezone-naive para Excel
        if not df.empty and 'fecha_creacion' in df.columns:
            df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion']).dt.tz_localize(None)
        
        # Crear archivo Excel
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relaciones de Usuarios', index=False)
            
                        # Resumen por tipo de relación
            if not df.empty:
                relationship_summary = df.groupby('tipo_relacion').agg({
                    'usuario_id': 'count'
                })
                relationship_summary.columns = ['Total Relaciones']
                relationship_summary.to_excel(writer, sheet_name='Resumen por Tipo')
                
                # Resumen por estado
                status_summary = df.groupby('estado_relacion').agg({
                    'usuario_id': 'count'
                })
                status_summary.columns = ['Total Relaciones']
                status_summary.to_excel(writer, sheet_name='Resumen por Estado')
        
        output.seek(0)
        
        # Generar nombre del archivo
        timestamp = datetime.now(pytz.timezone('America/Bogota')).strftime('%Y%m%d_%H%M%S')
        filename = f"reporte_relaciones_{timestamp}.xlsx"
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        ) 