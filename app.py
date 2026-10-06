import streamlit as st
from supabase import create_client
import pandas as pd
from io import BytesIO
from datetime import datetime, date

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Hydraulic & Hidrostatic | Inventarios",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SUPABASE
# =========================================================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
)

# =========================================================
# ESTILOS
# =========================================================
st.markdown("""
<style>

/* =====================================================
   CONFIGURACIÓN GENERAL
===================================================== */

.stApp {
    background: #f7f8fa;
}

.block-container {
    padding-top: 1.3rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e7e7e7;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

section[data-testid="stSidebar"] img {
    margin-bottom: 5px;
}

/* Texto MENÚ PRINCIPAL */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #888888;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Opciones del menú */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 5px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 10px 12px;
    border-radius: 9px;
    transition: 0.2s;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #fff0e7;
}

/* Opción seleccionada */
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(
        90deg,
        #f36c21,
        #ff7e32
    );
}

section[data-testid="stSidebar"]
div[role="radiogroup"]
label:has(input:checked) p {
    color: white !important;
    font-weight: 700;
}

/* Ocultar círculos del radio */
section[data-testid="stSidebar"] div[role="radiogroup"] input {
    display: none;
}
/* Ocultar completamente los círculos del menú */
section[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] [role="radiogroup"] label {
    gap: 0 !important;
}

/* =====================================================
   FRANJA SUPERIOR
===================================================== */

.barra-superior {
    height: 68px;
    margin: -22px -15px 25px -15px;

    background:
        linear-gradient(
            125deg,
            #f36c21 0%,
            #ff873d 17%,
            #ffd2b8 17%,
            #fff1e8 32%,
            #ffffff 32%
        );

    border-bottom: 3px solid #f36c21;
    border-radius: 0 0 8px 8px;
}

/* =====================================================
   ENCABEZADOS
===================================================== */

.titulo-pagina {
    color: #20252b;
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 3px;
}

.subtitulo-pagina {
    color: #7a7f85;
    font-size: 14px;
    margin-bottom: 20px;
}

.linea-titulo {
    width: 65px;
    height: 4px;
    background: #f36c21;
    border-radius: 10px;
    margin: 8px 0 22px 0;
}

/* =====================================================
   TARJETAS INDICADORES
===================================================== */

.kpi {
    background: #ffffff;
    border: 1px solid #eeeeee;
    border-radius: 16px;
    padding: 20px;

    min-height: 145px;

    box-shadow:
        0 4px 14px rgba(0,0,0,0.055);

    position: relative;
    overflow: hidden;
}

.kpi::after {
    content: "";
    position: absolute;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    right: -25px;
    bottom: -30px;
    background: rgba(243,108,33,0.07);
}

.kpi-icono {
    width: 43px;
    height: 43px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background: #fff1e8;

    font-size: 22px;
    margin-bottom: 12px;
}

.kpi-titulo {
    color: #687078;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

.kpi-numero {
    color: #17191c;
    font-size: 29px;
    font-weight: 800;
    margin-top: 5px;
}

.kpi-sub {
    color: #999999;
    font-size: 11px;
}

/* =====================================================
   SECCIONES
===================================================== */

.seccion-titulo {
    color: #24272b;
    font-size: 20px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 14px;
}

.seccion-titulo span {
    color: #f36c21;
}

/* =====================================================
   ACCESOS
===================================================== */

.acceso {
    background: white;
    border: 1px solid #e9e9e9;
    border-radius: 14px;
    min-height: 130px;
    padding: 20px;
    text-align: center;

    box-shadow:
        0 3px 10px rgba(0,0,0,0.04);
}

.acceso-icono {
    font-size: 29px;
    margin-bottom: 8px;
}

.acceso-nombre {
    font-size: 15px;
    font-weight: 800;
    color: #282c31;
}

.acceso-texto {
    color: #858585;
    font-size: 12px;
    margin-top: 5px;
}

/* =====================================================
   CAJAS / CONTENEDORES
===================================================== */

.caja {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ededed;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}

/* =====================================================
   BOTONES
===================================================== */

.stButton > button,
.stFormSubmitButton > button {

    background: #f36c21;
    color: white;

    border: none;
    border-radius: 8px;

    font-weight: 700;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {

    background: #df5c13;
    color: white;
    border: none;
}

/* =====================================================
   TABS
===================================================== */

button[data-baseweb="tab"] {
    font-weight: 650;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #f36c21 !important;
}

/* =====================================================
   FOOTER PERSONALIZADO
===================================================== */

.footer-app {
    margin-top: 45px;
    border-top: 1px solid #e8e8e8;
    padding-top: 15px;

    color: #969696;
    font-size: 11px;

    display: flex;
    justify-content: space-between;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CONSULTAR PRODUCTOS
# =========================================================
try:

    respuesta = (
        supabase
        .table("productos")
        .select("*")
        .order("id")
        .execute()
    )

    productos = respuesta.data

except Exception as e:

    st.error(
        f"No se pudo conectar con la base de datos: {e}"
    )

    st.stop()


productos_activos = [
    p for p in productos
    if p.get("estado") == "Activo"
]

# =========================================================
# INDICADORES
# =========================================================
total_productos = len(productos_activos)

total_unidades = sum(
    float(p.get("stock_actual") or 0)
    for p in productos_activos
)

stock_bajo = sum(
    1
    for p in productos_activos
    if float(p.get("stock_actual") or 0)
    <= float(p.get("stock_minimo") or 0)
)

sobrestock = sum(
    1
    for p in productos_activos
    if float(p.get("stock_maximo") or 0) > 0
    and float(p.get("stock_actual") or 0)
    > float(p.get("stock_maximo") or 0)
)

valor_inventario = sum(
    float(p.get("stock_actual") or 0)
    * float(p.get("precio_compra") or 0)
    for p in productos_activos
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.image(
        "assets/logo_hydraulic.png",
        use_container_width=True
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:11px;
            color:#888;
            margin-top:-5px;
            margin-bottom:15px;
            font-weight:600;
        ">
        SISTEMA DE CONTROL DE INVENTARIOS
        </div>
        """,
        unsafe_allow_html=True
    )

    opcion = st.radio(
        "MENÚ PRINCIPAL",
        [
            "🏠  Inicio",
            "📦  Productos",
            "📊  Inventario",
            "⬇️  Entradas",
            "⬆️  Salidas",
            "🔄  Movimientos / Kardex",
            "📋  Requerimientos",
            "📍  Ubicaciones",
            "📈  Reportes"
        ]
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#999;
            font-size:11px;
            line-height:1.7;
        ">
            Hydraulic and Hidrostatic E.I.R.L.<br>
            Callao - 2026
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# DECORACIÓN SUPERIOR
# =========================================================
st.markdown(
    '<div class="barra-superior"></div>',
    unsafe_allow_html=True
)

# =========================================================
# INICIO
# =========================================================
# =========================================================
# FUNCIONES PARA LOS MÓDULOS OPERATIVOS
# =========================================================
def titulo_modulo(texto):
    st.markdown(f'<div class="titulo-pagina">{texto}</div>', unsafe_allow_html=True)
    st.markdown('<div class="linea-titulo"></div>', unsafe_allow_html=True)


def excel_bytes(df, hoja="Reporte"):
    salida = BytesIO()
    df2 = df.copy()
    for c in df2.columns:
        if pd.api.types.is_datetime64_any_dtype(df2[c]):
            df2[c] = df2[c].astype(str)
    with pd.ExcelWriter(salida, engine="openpyxl") as writer:
        df2.to_excel(writer, index=False, sheet_name=hoja[:31])
    return salida.getvalue()


def etiqueta_producto(p):
    return f'{p.get("modelo") or "S/M"} | {p.get("producto") or "Sin nombre"} | {p.get("marca") or "Sin marca"} | ID {p.get("id")}'


def cargar_tabla(nombre, orden=None):
    try:
        q = supabase.table(nombre).select("*")
        if orden:
            q = q.order(orden, desc=True)
        return q.execute().data or []
    except Exception as e:
        st.error(f"No se pudo consultar {nombre}: {e}")
        return []


def mostrar_descarga(df, nombre, hoja):
    if not df.empty:
        st.download_button(
            "📥 Descargar Excel",
            data=excel_bytes(df, hoja),
            file_name=nombre,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def flash():
    if st.session_state.get("flash"):
        st.success(st.session_state.pop("flash"))



if opcion == "🏠  Inicio":

    # -----------------------------------------------------
    # BANNER REAL
    # -----------------------------------------------------
    st.image(
        "assets/banner_hydraulic.png",
        use_container_width=True
    )

    st.write("")

    # -----------------------------------------------------
    # INDICADORES
    # -----------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-icono">📦</div>
<div class="kpi-titulo">Productos activos</div>
<div class="kpi-numero">{total_productos}</div>
<div class="kpi-sub">Productos registrados</div>
</div>
""",
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-icono">▦</div>
<div class="kpi-titulo">Unidades en stock</div>
<div class="kpi-numero">{total_unidades:,.0f}</div>
<div class="kpi-sub">Existencias registradas</div>
</div>
""",
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-icono">⚠️</div>
<div class="kpi-titulo">Stock bajo</div>
<div class="kpi-numero">{stock_bajo}</div>
<div class="kpi-sub">Productos por reponer</div>
</div>
""",
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-icono">📈</div>
<div class="kpi-titulo">Sobrestock</div>
<div class="kpi-numero">{sobrestock}</div>
<div class="kpi-sub">Sobre el stock máximo</div>
</div>
""",
            unsafe_allow_html=True
        )

    with c5:

        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-icono">S/</div>
<div class="kpi-titulo">Valor inventario</div>
<div class="kpi-numero" style="font-size:21px;">
S/ {valor_inventario:,.2f}
</div>
<div class="kpi-sub">Según precio de compra</div>
</div>
""",
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # ACCESOS
    # -----------------------------------------------------
    st.markdown(
        """
<div class="seccion-titulo">
<span>▦</span> Accesos rápidos
</div>
""",
        unsafe_allow_html=True
    )

    a1, a2, a3, a4, a5, a6 = st.columns(6)

    with a1:
        st.markdown("""
<div class="acceso">
<div class="acceso-icono">📊</div>
<div class="acceso-nombre">Inventario</div>
<div class="acceso-texto">Consulta de existencias</div>
</div>
""", unsafe_allow_html=True)

    with a2:
        st.markdown("""
<div class="acceso">
<div class="acceso-icono">📦</div>
<div class="acceso-nombre">Productos</div>
<div class="acceso-texto">Catálogo de productos</div>
</div>
""", unsafe_allow_html=True)

    with a3:
        st.markdown("""
<div class="acceso">
<div class="acceso-icono">⬇️</div>
<div class="acceso-nombre">Entradas</div>
<div class="acceso-texto">Ingreso de existencias</div>
</div>
""", unsafe_allow_html=True)

    with a4:
        st.markdown("""
<div class="acceso">
<div class="acceso-icono">⬆️</div>
<div class="acceso-nombre">Salidas</div>
<div class="acceso-texto">Salida de existencias</div>
</div>
""", unsafe_allow_html=True)

    with a5:
        st.markdown("""
<div class="acceso">
<div class="acceso-icono">🔄</div>
<div class="acceso-nombre">Kardex</div>
<div class="acceso-texto">Historial de movimientos</div>
</div>
""", unsafe_allow_html=True)

    with a6:
        st.markdown("""
<div class="acceso">
<div class="acceso-icono">📈</div>
<div class="acceso-nombre">Reportes</div>
<div class="acceso-texto">Indicadores y resultados</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(
        """
<div class="footer-app">
<span>
© 2026 Hydraulic and Hidrostatic E.I.R.L. |
Sistema de Control de Inventarios
</span>
<span>📍 Callao, Perú</span>
</div>
""",
        unsafe_allow_html=True
    )

# =========================================================
# PRODUCTOS
# =========================================================
elif opcion == "📦  Productos":

    st.markdown(
        '<div class="titulo-pagina">Gestión de Productos</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo-pagina">'
        'Consulta y administración del catálogo de productos.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="linea-titulo"></div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Consultar",
        "➕ Agregar",
        "✏️ Editar",
        "🗑️ Desactivar"
    ])

    # -----------------------------------------------------
    # CONSULTAR
    # -----------------------------------------------------
    with tab1:

        f1, f2, f3 = st.columns([2, 1, 1])

        with f1:
            buscar = st.text_input(
                "Buscar producto",
                placeholder=(
                    "Modelo, serie, producto, marca, "
                    "proveedor o ubicación..."
                )
            )

        categorias = sorted({
            str(p.get("categoria"))
            for p in productos_activos
            if p.get("categoria")
        })

        with f2:
            categoria = st.selectbox(
                "Categoría",
                ["Todas"] + categorias
            )

        with f3:
            estado_filtro = st.selectbox(
                "Estado de stock",
                [
                    "Todos",
                    "NORMAL",
                    "STOCK BAJO",
                    "SOBRESTOCK"
                ]
            )

        filtrados = []

        for p in productos_activos:

            stock = float(p.get("stock_actual") or 0)
            minimo = float(p.get("stock_minimo") or 0)
            maximo = float(p.get("stock_maximo") or 0)

            if stock <= minimo:
                estado_stock = "STOCK BAJO"

            elif maximo > 0 and stock > maximo:
                estado_stock = "SOBRESTOCK"

            else:
                estado_stock = "NORMAL"

            texto = " ".join([
                str(p.get("modelo") or ""),
                str(p.get("serie") or ""),
                str(p.get("producto") or ""),
                str(p.get("marca") or ""),
                str(p.get("proveedor") or ""),
                str(p.get("ubicacion") or "")
            ]).lower()

            cumple_busqueda = (
                not buscar
                or buscar.lower() in texto
            )

            cumple_categoria = (
                categoria == "Todas"
                or p.get("categoria") == categoria
            )

            cumple_estado = (
                estado_filtro == "Todos"
                or estado_stock == estado_filtro
            )

            if (
                cumple_busqueda
                and cumple_categoria
                and cumple_estado
            ):
                registro = p.copy()
                registro["estado_stock"] = estado_stock
                filtrados.append(registro)

        st.caption(
            f"Mostrando {len(filtrados)} de "
            f"{total_productos} productos activos"
        )

        if filtrados:

            df = pd.DataFrame(filtrados)

            columnas = [
                "modelo",
                "serie",
                "producto",
                "categoria",
                "marca",
                "proveedor",
                "unidad",
                "stock_actual",
                "stock_minimo",
                "stock_maximo",
                "estado_stock",
                "ubicacion",
                "precio_compra",
                "precio_venta"
            ]

            df = df[columnas]

            df.columns = [
                "Modelo",
                "Serie",
                "Producto",
                "Categoría",
                "Marca",
                "Proveedor",
                "Unidad",
                "Stock actual",
                "Stock mínimo",
                "Stock máximo",
                "Estado stock",
                "Ubicación",
                "Precio compra S/",
                "Precio venta S/"
            ]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=520
            )

        else:

            st.warning(
                "No se encontraron productos."
            )

    # -----------------------------------------------------
    # AGREGAR
    # -----------------------------------------------------
    with tab2:

        st.subheader("Registrar nuevo producto")

        st.info(
            "El nuevo producto iniciará con stock 0. "
            "El stock se incrementará mediante Entradas."
        )

        with st.form("nuevo_producto"):

            col1, col2 = st.columns(2)

            with col1:

                modelo = st.text_input("Modelo *")
                serie = st.text_input("Serie")
                nombre = st.text_input("Producto *")
                categoria_nueva = st.text_input("Categoría")
                marca = st.text_input("Marca")
                proveedor = st.text_input("Proveedor")
                pais = st.text_input("País de origen")

            with col2:

                unidad = st.text_input(
                    "Unidad de medida *",
                    value="Unidad"
                )

                ubicacion = st.text_input("Ubicación")

                minimo = st.number_input(
                    "Stock mínimo",
                    min_value=0.0,
                    step=1.0
                )

                maximo = st.number_input(
                    "Stock máximo",
                    min_value=0.0,
                    step=1.0
                )

                precio_compra = st.number_input(
                    "Precio compra S/",
                    min_value=0.0,
                    step=1.0
                )

                precio_venta = st.number_input(
                    "Precio venta S/",
                    min_value=0.0,
                    step=1.0
                )

            especificacion = st.text_area(
                "Especificación técnica"
            )

            guardar = st.form_submit_button(
                "Guardar producto",
                use_container_width=True
            )

        if guardar:

            if not modelo.strip():

                st.error(
                    "El modelo es obligatorio."
                )

            elif not nombre.strip():

                st.error(
                    "El nombre del producto es obligatorio."
                )

            elif not unidad.strip():

                st.error(
                    "La unidad de medida es obligatoria."
                )

            elif maximo > 0 and maximo < minimo:

                st.error(
                    "El stock máximo no puede ser "
                    "menor que el mínimo."
                )

            else:

                try:

                    datos = {
                        "modelo": modelo.strip(),
                        "serie": serie.strip() or None,
                        "producto": nombre.strip(),
                        "categoria":
                            categoria_nueva.strip() or None,
                        "marca": marca.strip() or None,
                        "proveedor":
                            proveedor.strip() or None,
                        "pais_origen":
                            pais.strip() or None,
                        "especificacion_tecnica":
                            especificacion.strip() or None,
                        "unidad": unidad.strip(),
                        "stock_actual": 0,
                        "stock_minimo": minimo,
                        "stock_maximo": maximo,
                        "ubicacion":
                            ubicacion.strip() or None,
                        "precio_compra":
                            precio_compra,
                        "precio_venta":
                            precio_venta,
                        "estado": "Activo"
                    }

                    (
                        supabase
                        .table("productos")
                        .insert(datos)
                        .execute()
                    )

                    st.success(
                        "Producto registrado correctamente."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"No se pudo registrar: {e}"
                    )

    # -----------------------------------------------------
    # EDITAR
    # -----------------------------------------------------
    with tab3:

        st.subheader("Editar producto")

        st.caption(
            "El stock no se modifica aquí. "
            "Se modifica mediante Entradas y Salidas."
        )

        opciones = {
            (
                f"{p.get('modelo')} | "
                f"{p.get('producto')} | "
                f"ID {p.get('id')}"
            ): p
            for p in productos_activos
        }

        seleccion = st.selectbox(
            "Seleccionar producto",
            list(opciones.keys())
        )

        p = opciones[seleccion]

        st.info(
            f"Stock actual: "
            f"{float(p.get('stock_actual') or 0):,.2f} "
            f"{p.get('unidad') or ''}"
        )

        with st.form("editar_producto"):

            e1, e2 = st.columns(2)

            with e1:

                emodelo = st.text_input(
                    "Modelo *",
                    value=str(p.get("modelo") or "")
                )

                eserie = st.text_input(
                    "Serie",
                    value=str(p.get("serie") or "")
                )

                enombre = st.text_input(
                    "Producto *",
                    value=str(p.get("producto") or "")
                )

                ecategoria = st.text_input(
                    "Categoría",
                    value=str(p.get("categoria") or "")
                )

                emarca = st.text_input(
                    "Marca",
                    value=str(p.get("marca") or "")
                )

                eproveedor = st.text_input(
                    "Proveedor",
                    value=str(p.get("proveedor") or "")
                )

            with e2:

                eunidad = st.text_input(
                    "Unidad *",
                    value=str(p.get("unidad") or "Unidad")
                )

                eubicacion = st.text_input(
                    "Ubicación",
                    value=str(p.get("ubicacion") or "")
                )

                eminimo = st.number_input(
                    "Stock mínimo",
                    min_value=0.0,
                    value=float(
                        p.get("stock_minimo") or 0
                    ),
                    step=1.0
                )

                emaximo = st.number_input(
                    "Stock máximo",
                    min_value=0.0,
                    value=float(
                        p.get("stock_maximo") or 0
                    ),
                    step=1.0
                )

                ecompra = st.number_input(
                    "Precio compra S/",
                    min_value=0.0,
                    value=float(
                        p.get("precio_compra") or 0
                    ),
                    step=1.0
                )

                eventa = st.number_input(
                    "Precio venta S/",
                    min_value=0.0,
                    value=float(
                        p.get("precio_venta") or 0
                    ),
                    step=1.0
                )

            actualizar = st.form_submit_button(
                "Guardar cambios",
                use_container_width=True
            )

        if actualizar:

            if not emodelo.strip() or not enombre.strip():

                st.error(
                    "Modelo y producto son obligatorios."
                )

            elif emaximo > 0 and emaximo < eminimo:

                st.error(
                    "El stock máximo no puede ser "
                    "menor que el mínimo."
                )

            else:

                try:

                    cambios = {
                        "modelo": emodelo.strip(),
                        "serie": eserie.strip() or None,
                        "producto": enombre.strip(),
                        "categoria":
                            ecategoria.strip() or None,
                        "marca":
                            emarca.strip() or None,
                        "proveedor":
                            eproveedor.strip() or None,
                        "unidad": eunidad.strip(),
                        "ubicacion":
                            eubicacion.strip() or None,
                        "stock_minimo": eminimo,
                        "stock_maximo": emaximo,
                        "precio_compra": ecompra,
                        "precio_venta": eventa
                    }

                    (
                        supabase
                        .table("productos")
                        .update(cambios)
                        .eq("id", p["id"])
                        .execute()
                    )

                    st.success(
                        "Producto actualizado correctamente."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"No se pudo actualizar: {e}"
                    )


    # -----------------------------------------------------
    # DESACTIVAR
    # -----------------------------------------------------
    with tab4:

        st.subheader("Desactivar producto")
        st.caption(
            "El producto no se elimina de la base de datos. "
            "Se conservará su historial y quedará inactivo para nuevas operaciones."
        )

        if not productos_activos:
            st.info("No existen productos activos para desactivar.")
        else:
            opciones_desactivar = {
                etiqueta_producto(p): p
                for p in productos_activos
            }

            seleccion_desactivar = st.selectbox(
                "Seleccionar producto *",
                list(opciones_desactivar.keys()),
                key="producto_desactivar"
            )

            producto_desactivar = opciones_desactivar[seleccion_desactivar]

            st.info(
                f'Stock actual: {float(producto_desactivar.get("stock_actual") or 0):g} '
                f'{producto_desactivar.get("unidad") or "unid."}'
            )

            confirmar_desactivar = st.checkbox(
                "Confirmo que deseo desactivar este producto.",
                key="confirmar_desactivar_producto"
            )

            if st.button(
                "🗑️ Desactivar producto",
                use_container_width=True,
                key="btn_desactivar_producto"
            ):
                if not confirmar_desactivar:
                    st.error("Confirme la desactivación del producto.")
                else:
                    try:
                        (
                            supabase
                            .table("productos")
                            .update({"estado": "Inactivo"})
                            .eq("id", producto_desactivar["id"])
                            .execute()
                        )
                        st.session_state["flash"] = (
                            f'Producto desactivado correctamente: '
                            f'{producto_desactivar.get("producto")}.'
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"No se pudo desactivar el producto: {e}")


# =========================================================
# INVENTARIO
# =========================================================
elif opcion == "📊  Inventario":

    st.markdown(
        '<div class="titulo-pagina">📊 Inventario</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo-pagina">'
        'Consulta y control de las existencias actuales del almacén.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="linea-titulo"></div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # RESUMEN DEL INVENTARIO
    # -----------------------------------------------------
    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.metric(
            "Productos activos",
            f"{total_productos}"
        )

    with r2:
        st.metric(
            "Unidades en stock",
            f"{total_unidades:,.0f}"
        )

    with r3:
        st.metric(
            "Stock bajo",
            f"{stock_bajo}"
        )

    with r4:
        st.metric(
            "Sobrestock",
            f"{sobrestock}"
        )

    st.write("")

    # -----------------------------------------------------
    # FILTROS
    # -----------------------------------------------------
    st.markdown(
        """
<div class="seccion-titulo">
<span>⌕</span> Consulta de existencias
</div>
""",
        unsafe_allow_html=True
    )

    col_buscar, col_categoria, col_estado = st.columns(
        [2, 1, 1]
    )

    with col_buscar:

        buscar_inventario = st.text_input(
            "Buscar",
            placeholder=(
                "Modelo, serie, producto, marca "
                "o ubicación..."
            ),
            key="buscar_inventario"
        )

    categorias_inventario = sorted({
        str(p.get("categoria"))
        for p in productos_activos
        if p.get("categoria")
    })

    with col_categoria:

        categoria_inventario = st.selectbox(
            "Categoría",
            ["Todas"] + categorias_inventario,
            key="categoria_inventario"
        )

    with col_estado:

        estado_inventario = st.selectbox(
            "Estado de stock",
            [
                "Todos",
                "NORMAL",
                "STOCK BAJO",
                "SOBRESTOCK"
            ],
            key="estado_inventario"
        )

    # -----------------------------------------------------
    # PREPARAR INVENTARIO
    # -----------------------------------------------------
    inventario_filtrado = []

    for p in productos_activos:

        stock = float(
            p.get("stock_actual") or 0
        )

        minimo = float(
            p.get("stock_minimo") or 0
        )

        maximo = float(
            p.get("stock_maximo") or 0
        )

        if stock <= minimo:

            estado_stock = "STOCK BAJO"

        elif maximo > 0 and stock > maximo:

            estado_stock = "SOBRESTOCK"

        else:

            estado_stock = "NORMAL"

        texto_busqueda = " ".join([
            str(p.get("modelo") or ""),
            str(p.get("serie") or ""),
            str(p.get("producto") or ""),
            str(p.get("categoria") or ""),
            str(p.get("marca") or ""),
            str(p.get("ubicacion") or "")
        ]).lower()

        cumple_busqueda = (
            not buscar_inventario
            or buscar_inventario.lower()
            in texto_busqueda
        )

        cumple_categoria = (
            categoria_inventario == "Todas"
            or p.get("categoria")
            == categoria_inventario
        )

        cumple_estado = (
            estado_inventario == "Todos"
            or estado_stock
            == estado_inventario
        )

        if (
            cumple_busqueda
            and cumple_categoria
            and cumple_estado
        ):

            valor_producto = (
                stock
                * float(
                    p.get("precio_compra") or 0
                )
            )

            inventario_filtrado.append({
                "Modelo":
                    p.get("modelo"),

                "Serie":
                    p.get("serie"),

                "Producto":
                    p.get("producto"),

                "Categoría":
                    p.get("categoria"),

                "Marca":
                    p.get("marca"),

                "Unidad":
                    p.get("unidad"),

                "Stock actual":
                    stock,

                "Stock mínimo":
                    minimo,

                "Stock máximo":
                    maximo,

                "Estado":
                    estado_stock,

                "Ubicación":
                    p.get("ubicacion"),

                "Precio compra S/":
                    float(
                        p.get("precio_compra")
                        or 0
                    ),

                "Valor inventario S/":
                    valor_producto
            })

    # -----------------------------------------------------
    # RESULTADOS
    # -----------------------------------------------------
    st.caption(
        f"Mostrando {len(inventario_filtrado)} "
        f"de {total_productos} productos."
    )

    if inventario_filtrado:

        df_inventario = pd.DataFrame(
            inventario_filtrado
        )

        st.dataframe(
            df_inventario,
            use_container_width=True,
            hide_index=True,
            height=520,
            column_config={
                "Stock actual":
                    st.column_config.NumberColumn(
                        format="%.0f"
                    ),

                "Stock mínimo":
                    st.column_config.NumberColumn(
                        format="%.0f"
                    ),

                "Stock máximo":
                    st.column_config.NumberColumn(
                        format="%.0f"
                    ),

                "Precio compra S/":
                    st.column_config.NumberColumn(
                        format="S/ %.2f"
                    ),

                "Valor inventario S/":
                    st.column_config.NumberColumn(
                        format="S/ %.2f"
                    )
            }
        )

        # -------------------------------------------------
        # RESUMEN DE LO FILTRADO
        # -------------------------------------------------
        unidades_filtradas = (
            df_inventario["Stock actual"].sum()
        )

        valor_filtrado = (
            df_inventario[
                "Valor inventario S/"
            ].sum()
        )

        s1, s2, s3 = st.columns(3)

        with s1:
            st.metric(
                "Productos mostrados",
                len(df_inventario)
            )

        with s2:
            st.metric(
                "Unidades mostradas",
                f"{unidades_filtradas:,.0f}"
            )

        with s3:
            st.metric(
                "Valor mostrado",
                f"S/ {valor_filtrado:,.2f}"
            )

    else:

        st.warning(
            "No existen productos que coincidan "
            "con los filtros seleccionados."
        )

    # -----------------------------------------------------
    # ACLARACIÓN
    # -----------------------------------------------------
    st.info(
        "ℹ️ El stock mostrado corresponde a las existencias "
        "registradas en el sistema. Las cantidades no se "
        "modifican directamente desde Inventario; los cambios "
        "se realizarán mediante los módulos Entradas y Salidas."
    )
# =========================================================
# ENTRADAS
# =========================================================
elif opcion == "⬇️  Entradas":
    titulo_modulo("Entradas de inventario")
    flash()
    st.caption("Registra el ingreso de productos al almacén. El stock se actualiza automáticamente.")

    if not productos_activos:
        st.warning("No existen productos activos.")
    else:
        mapa = {etiqueta_producto(p): p for p in productos_activos}
        with st.form("form_entrada", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                sel = st.selectbox("Producto *", list(mapa.keys()))
                cantidad = st.number_input("Cantidad *", min_value=1.0, step=1.0)
                motivo = st.selectbox("Motivo *", ["Compra", "Devolución", "Regularización", "Otro"])
            with c2:
                documento = st.text_input("Documento / referencia")
                responsable = st.text_input("Responsable *")
                fecha_mov = st.date_input("Fecha", value=date.today())
            otro = st.text_input("Especifique el motivo") if motivo == "Otro" else ""
            guardar = st.form_submit_button("✅ Registrar entrada", use_container_width=True)
        if guardar:
            if not responsable.strip():
                st.error("Ingrese el responsable.")
            elif motivo == "Otro" and not otro.strip():
                st.error("Especifique el motivo.")
            else:
                p = mapa[sel]
                try:
                    supabase.rpc("registrar_movimiento", {
                        "p_producto_id": p["id"], "p_tipo_movimiento": "ENTRADA",
                        "p_cantidad": cantidad, "p_motivo": otro.strip() if motivo == "Otro" else motivo,
                        "p_documento": documento.strip() or None, "p_area_destino": None,
                        "p_responsable": responsable.strip(), "p_requerimiento_id": None,
                        "p_fecha_movimiento": f"{fecha_mov.isoformat()}T12:00:00-05:00"
                    }).execute()
                    st.session_state["flash"] = f"Entrada registrada correctamente: {cantidad:g} {p.get('unidad') or 'unid.'} de {p.get('producto')}."
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudo registrar la entrada: {e}")

    movimientos = cargar_tabla("movimientos", "fecha_movimiento")
    entradas = [m for m in movimientos if str(m.get("tipo_movimiento", "")).upper() == "ENTRADA"]
    if entradas:
        nombres = {p["id"]: etiqueta_producto(p) for p in productos}
        df = pd.DataFrame(entradas)
        if "producto_id" in df: df.insert(1, "Producto", df["producto_id"].map(nombres))
        st.subheader("Últimas entradas")
        st.dataframe(df, use_container_width=True, hide_index=True)
        mostrar_descarga(df, "entradas_inventario.xlsx", "Entradas")

# =========================================================
# SALIDAS
# =========================================================
elif opcion == "⬆️  Salidas":
    titulo_modulo("Salidas de inventario")
    flash()
    st.caption("Registra salidas del almacén con validación de existencias.")
    disponibles = [p for p in productos_activos if float(p.get("stock_actual") or 0) > 0]
    if not disponibles:
        st.warning("No existen productos con stock disponible.")
    else:
        mapa = {etiqueta_producto(p): p for p in disponibles}
        sel = st.selectbox("Producto *", list(mapa.keys()), key="sal_prod")
        psel = mapa[sel]
        st.info(f'Stock disponible: {float(psel.get("stock_actual") or 0):g} {psel.get("unidad") or "unid."}')
        with st.form("form_salida", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                cantidad = st.number_input("Cantidad *", min_value=1.0, step=1.0)
                motivo = st.selectbox("Motivo *", ["Atención de requerimiento", "Uso interno", "Devolución a proveedor", "Regularización", "Otro"])
                destino = st.text_input("Área / destino *")
            with c2:
                documento = st.text_input("Documento / referencia")
                responsable = st.text_input("Responsable")
                fecha_mov = st.date_input("Fecha", value=date.today(), key="fecha_salida")
            otro = st.text_input("Especifique el motivo") if motivo == "Otro" else ""
            guardar = st.form_submit_button("✅ Registrar salida", use_container_width=True)
        if guardar:
            stock = float(psel.get("stock_actual") or 0)
            if cantidad > stock:
                st.error(f"La cantidad supera el stock disponible ({stock:g}).")
            elif not destino.strip():
                st.error("Complete el área/destino.")
            elif motivo == "Otro" and not otro.strip():
                st.error("Especifique el motivo.")
            else:
                try:
                    supabase.rpc("registrar_movimiento", {
                        "p_producto_id": psel["id"], "p_tipo_movimiento": "SALIDA",
                        "p_cantidad": cantidad, "p_motivo": otro.strip() if motivo == "Otro" else motivo,
                        "p_documento": documento.strip() or None, "p_area_destino": destino.strip(),
                        "p_responsable": responsable.strip() or None, "p_requerimiento_id": None,
                        "p_fecha_movimiento": f"{fecha_mov.isoformat()}T12:00:00-05:00"
                    }).execute()
                    st.session_state["flash"] = f"Salida registrada correctamente: {cantidad:g} {psel.get('unidad') or 'unid.'} de {psel.get('producto')}."
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudo registrar la salida: {e}")

    movimientos = cargar_tabla("movimientos", "fecha_movimiento")
    salidas = [m for m in movimientos if str(m.get("tipo_movimiento", "")).upper() == "SALIDA"]
    if salidas:
        nombres = {p["id"]: etiqueta_producto(p) for p in productos}
        df = pd.DataFrame(salidas)
        if "producto_id" in df: df.insert(1, "Producto", df["producto_id"].map(nombres))
        st.subheader("Últimas salidas")
        st.dataframe(df, use_container_width=True, hide_index=True)
        mostrar_descarga(df, "salidas_inventario.xlsx", "Salidas")

# =========================================================
# MOVIMIENTOS / KARDEX
# =========================================================
elif opcion == "🔄  Movimientos / Kardex":
    titulo_modulo("Movimientos / Kardex")
    movs = cargar_tabla("movimientos", "fecha_movimiento")
    if not movs:
        st.info("Aún no existen movimientos registrados.")
    else:
        nombres = {p["id"]: etiqueta_producto(p) for p in productos}
        df = pd.DataFrame(movs)
        if "producto_id" in df: df.insert(1, "Producto", df["producto_id"].map(nombres))
        c1, c2 = st.columns(2)
        tipos = ["Todos"] + sorted(df["tipo_movimiento"].dropna().astype(str).unique().tolist()) if "tipo_movimiento" in df else ["Todos"]
        tipo = c1.selectbox("Tipo", tipos)
        buscar = c2.text_input("Buscar producto, documento o responsable")
        filtrado = df.copy()
        if tipo != "Todos" and "tipo_movimiento" in filtrado:
            filtrado = filtrado[filtrado["tipo_movimiento"].astype(str) == tipo]
        if buscar.strip():
            texto = filtrado.astype(str).agg(" ".join, axis=1)
            filtrado = filtrado[texto.str.contains(buscar.strip(), case=False, na=False)]
        st.caption(f"{len(filtrado)} movimiento(s) encontrado(s).")
        st.dataframe(filtrado, use_container_width=True, hide_index=True, height=520)
        mostrar_descarga(filtrado, "kardex_movimientos.xlsx", "Kardex")

# =========================================================
# REQUERIMIENTOS
# =========================================================
elif opcion == "📋  Requerimientos":
    titulo_modulo("Requerimientos internos")
    flash()
    st.caption("Registra y realiza el seguimiento de los requerimientos internos del almacén.")

    # Consulta directa para que las pestañas siempre tengan contenido visible.
    try:
        reqs = (
            supabase.table("requerimientos")
            .select("*")
            .order("fecha_solicitud", desc=True)
            .execute()
            .data or []
        )
        error_reqs = None
    except Exception as e:
        reqs = []
        error_reqs = str(e)

    tabs = st.tabs(["📋 Consultar", "➕ Registrar", "🔄 Actualizar estado"])

    # -----------------------------------------------------
    # CONSULTAR
    # -----------------------------------------------------
    with tabs[0]:
        st.subheader("Consulta de requerimientos")

        if error_reqs:
            st.error(f"No se pudieron consultar los requerimientos: {error_reqs}")
        elif not reqs:
            st.info("Aún no existen requerimientos registrados. Puedes crear el primero en la pestaña ➕ Registrar.")
        else:
            # Filtros de cabecera
            f1, f2 = st.columns([2, 1])
            buscar_req = f1.text_input(
                "Buscar",
                placeholder="N.º de requerimiento, área, responsable, motivo...",
                key="buscar_requerimiento"
            )
            estados_existentes = sorted({
                str(r.get("estado")) for r in reqs if r.get("estado")
            })
            estado_req = f2.selectbox(
                "Estado", ["Todos"] + estados_existentes, key="filtro_estado_req"
            )

            reqs_filtrados = []
            for r in reqs:
                if estado_req != "Todos" and str(r.get("estado") or "") != estado_req:
                    continue
                texto = " ".join([
                    str(r.get("numero_requerimiento") or ""),
                    str(r.get("area_solicitante") or ""),
                    str(r.get("responsable") or ""),
                    str(r.get("motivo") or ""),
                    str(r.get("estado") or "")
                ]).lower()
                if buscar_req.strip() and buscar_req.strip().lower() not in texto:
                    continue
                reqs_filtrados.append(r)

            st.caption(f"{len(reqs_filtrados)} requerimiento(s) encontrado(s).")

            if not reqs_filtrados:
                st.warning("No existen requerimientos que coincidan con los filtros seleccionados.")
            else:
                # Tabla resumen
                filas_resumen = []
                for r in reqs_filtrados:
                    filas_resumen.append({
                        "N.º requerimiento": r.get("numero_requerimiento"),
                        "Fecha de solicitud": r.get("fecha_solicitud"),
                        "Área solicitante": r.get("area_solicitante"),
                        "Motivo / descripción": r.get("motivo"),
                        "Responsable": r.get("responsable"),
                        "Estado": r.get("estado"),
                        "Inicio de preparación": r.get("fecha_inicio_preparacion"),
                        "Fecha de entrega": r.get("fecha_entrega"),
                        "Entrega completa": r.get("entrega_completa"),
                        "Observaciones": r.get("observaciones")
                    })
                df_resumen = pd.DataFrame(filas_resumen)
                st.dataframe(df_resumen, use_container_width=True, hide_index=True, height=330)
                mostrar_descarga(df_resumen, "requerimientos.xlsx", "Requerimientos")

                st.markdown("#### Detalle del requerimiento")
                mapa_consulta = {
                    (
                        f'{r.get("numero_requerimiento") or "S/N"} | '
                        f'{r.get("area_solicitante") or "Sin área"} | '
                        f'{r.get("estado") or "Sin estado"} | ID {r.get("id")}'
                    ): r
                    for r in reqs_filtrados
                }
                etiqueta_req = st.selectbox(
                    "Seleccionar requerimiento para ver sus productos",
                    list(mapa_consulta.keys()),
                    key="req_consultar_detalle"
                )
                req_sel = mapa_consulta[etiqueta_req]

                try:
                    detalles = (
                        supabase.table("requerimiento_detalle")
                        .select("*")
                        .eq("requerimiento_id", req_sel["id"])
                        .execute()
                        .data or []
                    )
                    error_detalle = None
                except Exception as e:
                    detalles = []
                    error_detalle = str(e)

                if error_detalle:
                    st.error(f"No se pudieron consultar los productos del requerimiento: {error_detalle}")
                elif not detalles:
                    st.info("Este requerimiento no tiene productos registrados en su detalle.")
                else:
                    productos_por_id = {p.get("id"): p for p in productos}
                    filas_detalle = []
                    for d in detalles:
                        p = productos_por_id.get(d.get("producto_id"), {})
                        filas_detalle.append({
                            "Modelo": p.get("modelo"),
                            "Serie": p.get("serie"),
                            "Producto": p.get("producto"),
                            "Marca": p.get("marca"),
                            "Unidad": p.get("unidad"),
                            "Cantidad solicitada": d.get("cantidad_solicitada"),
                            "Cantidad entregada": d.get("cantidad_entregada") or 0
                        })
                    df_detalle = pd.DataFrame(filas_detalle)
                    st.dataframe(df_detalle, use_container_width=True, hide_index=True)
                    mostrar_descarga(
                        df_detalle,
                        f'detalle_{req_sel.get("numero_requerimiento") or "requerimiento"}.xlsx',
                        "Detalle"
                    )
    # -----------------------------------------------------
    # REGISTRAR
    # -----------------------------------------------------
    with tabs[1]:
        st.subheader("Registrar requerimiento interno")
        st.caption("Registra los datos del requerimiento y los productos solicitados.")

        c1, c2 = st.columns(2)
        with c1:
            numero = st.text_input("N.º de requerimiento *", key="req_numero_nuevo")
            area = st.text_input("Área solicitante *", key="req_area_nueva")
            motivo = st.text_input("Motivo / descripción *", key="req_motivo_nuevo")
        with c2:
            responsable = st.text_input(
                "Responsable",
                key="req_responsable_nuevo",
                help="Opcional. Complétalo solo cuando se disponga de este dato."
            )
            observaciones = st.text_area("Observaciones", key="req_observaciones_nuevas")

        st.markdown("#### Productos solicitados")
        st.caption("Selecciona uno o varios productos y registra la cantidad solicitada de cada uno.")

        cantidad_productos = st.number_input(
            "Cantidad de productos diferentes *",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
            key="req_cantidad_productos"
        )

        mapa_productos_req = {
            etiqueta_producto(p): p for p in productos_activos
        }
        etiquetas_productos_req = list(mapa_productos_req.keys())
        detalle_nuevo = []

        if not etiquetas_productos_req:
            st.warning("No existen productos activos para agregar al requerimiento.")
        else:
            for i in range(int(cantidad_productos)):
                pc1, pc2 = st.columns([3, 1])
                with pc1:
                    producto_sel = st.selectbox(
                        f"Producto {i + 1} *",
                        etiquetas_productos_req,
                        key=f"req_producto_{i}"
                    )
                with pc2:
                    cantidad_sol = st.number_input(
                        f"Cantidad {i + 1} *",
                        min_value=1.0,
                        step=1.0,
                        value=1.0,
                        key=f"req_cantidad_{i}"
                    )
                detalle_nuevo.append((mapa_productos_req[producto_sel], cantidad_sol))

        guardar = st.button(
            "✅ Registrar requerimiento",
            use_container_width=True,
            key="btn_registrar_requerimiento"
        )

        if guardar:
            if not all([numero.strip(), area.strip(), motivo.strip()]):
                st.error("Complete N.º de requerimiento, área solicitante y motivo.")
            elif not detalle_nuevo:
                st.error("Agregue al menos un producto al requerimiento.")
            elif len({p["id"] for p, _ in detalle_nuevo}) != len(detalle_nuevo):
                st.error("No repita el mismo producto. Si necesita más cantidad, modifique su cantidad solicitada.")
            elif any(
                str(r.get("numero_requerimiento") or "").strip().lower()
                == numero.strip().lower()
                for r in reqs
            ):
                st.error("Ya existe un requerimiento con ese número.")
            else:
                requerimiento_creado = None
                try:
                    datos_req = {
                        "numero_requerimiento": numero.strip(),
                        "fecha_solicitud": datetime.now().astimezone().isoformat(),
                        "area_solicitante": area.strip(),
                        "motivo": motivo.strip(),
                        "responsable": responsable.strip() or None,
                        "estado": "Pendiente",
                        "observaciones": observaciones.strip() or None
                    }
                    respuesta_req = (
                        supabase.table("requerimientos")
                        .insert(datos_req)
                        .execute()
                    )
                    creados = respuesta_req.data or []
                    if not creados:
                        raise Exception("No se pudo obtener el ID del requerimiento registrado.")
                    requerimiento_creado = creados[0]
                    req_id = requerimiento_creado["id"]

                    filas_detalle = [
                        {
                            "requerimiento_id": req_id,
                            "producto_id": p["id"],
                            "cantidad_solicitada": cantidad,
                            "cantidad_entregada": 0
                        }
                        for p, cantidad in detalle_nuevo
                    ]
                    supabase.table("requerimiento_detalle").insert(filas_detalle).execute()

                    st.session_state["flash"] = (
                        f"Requerimiento {numero.strip()} registrado correctamente con "
                        f"{len(filas_detalle)} producto(s)."
                    )
                    st.rerun()
                except Exception as e:
                    # Si se creó la cabecera pero falló el detalle, se elimina la cabecera
                    # para no dejar un requerimiento incompleto.
                    if requerimiento_creado and requerimiento_creado.get("id"):
                        try:
                            supabase.table("requerimientos").delete().eq(
                                "id", requerimiento_creado["id"]
                            ).execute()
                        except Exception:
                            pass
                    st.error(f"No se pudo registrar el requerimiento completo: {e}")

    # -----------------------------------------------------
    # ACTUALIZAR ESTADO
    # -----------------------------------------------------
    with tabs[2]:
        st.subheader("Actualizar estado del requerimiento")

        if error_reqs:
            st.error(f"No se pudieron consultar los requerimientos: {error_reqs}")
        elif not reqs:
            st.info("No hay requerimientos registrados para actualizar.")
        else:
            mapa_req = {}
            for r in reqs:
                etiqueta = (
                    f'{r.get("numero_requerimiento") or "S/N"} | '
                    f'{r.get("area_solicitante") or "Sin área"} | '
                    f'{r.get("estado") or "Sin estado"} | ID {r.get("id")}'
                )
                mapa_req[etiqueta] = r

            elegido = st.selectbox(
                "Seleccionar requerimiento", list(mapa_req.keys()),
                key="req_actualizar"
            )
            r = mapa_req[elegido]

            d1, d2, d3 = st.columns(3)
            d1.metric("N.º requerimiento", str(r.get("numero_requerimiento") or "-"))
            d2.metric("Área", str(r.get("area_solicitante") or "-"))
            d3.metric("Estado actual", str(r.get("estado") or "-"))

            estados = ["Pendiente", "En preparación", "Atendido", "Anulado"]
            actual = str(r.get("estado") or "Pendiente")
            indice = estados.index(actual) if actual in estados else 0
            nuevo = st.selectbox(
                "Nuevo estado", estados, index=indice, key="nuevo_estado_req"
            )

            # Valores iniciales: conserva lo ya registrado; si no existe, propone ahora.
            ahora_local = datetime.now()

            def fecha_hora_existente(valor):
                if not valor:
                    return ahora_local.date(), ahora_local.time().replace(second=0, microsecond=0)
                try:
                    dt = datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
                    return dt.date(), dt.time().replace(second=0, microsecond=0, tzinfo=None)
                except Exception:
                    return ahora_local.date(), ahora_local.time().replace(second=0, microsecond=0)

            fecha_inicio = hora_inicio = None
            fecha_entrega = hora_entrega = None

            if nuevo in ["En preparación", "Atendido"]:
                fi, hi = fecha_hora_existente(r.get("fecha_inicio_preparacion"))
                st.markdown("#### Inicio de preparación")
                i1, i2 = st.columns(2)
                fecha_inicio = i1.date_input(
                    "Fecha de inicio *", value=fi, key="fecha_inicio_req"
                )
                hora_inicio = i2.time_input(
                    "Hora de inicio *", value=hi, key="hora_inicio_req"
                )

            entrega_completa = False
            if nuevo == "Atendido":
                fe, he = fecha_hora_existente(r.get("fecha_entrega"))
                st.markdown("#### Entrega")
                e1, e2 = st.columns(2)
                fecha_entrega = e1.date_input(
                    "Fecha de entrega *", value=fe, key="fecha_entrega_req"
                )
                hora_entrega = e2.time_input(
                    "Hora de entrega *", value=he, key="hora_entrega_req"
                )
                entrega_completa = st.checkbox(
                    "Entrega completa",
                    value=bool(r.get("entrega_completa", True)),
                    key="entrega_completa_req"
                )

            if nuevo == "Pendiente":
                st.caption("El requerimiento permanecerá pendiente y todavía no tendrá fechas de preparación o entrega.")
            elif nuevo == "En preparación":
                st.caption("Puedes usar la fecha y hora actuales o modificarlas si estás registrando un requerimiento anterior.")
            elif nuevo == "Atendido":
                st.caption("Registra el inicio de preparación y la fecha/hora real de entrega del requerimiento.")
            else:
                st.caption("El requerimiento quedará anulado y se conservará en el historial.")

            if st.button("💾 Actualizar estado", use_container_width=True):
                datos = {"estado": nuevo}

                if nuevo in ["En preparación", "Atendido"]:
                    inicio_iso = f"{fecha_inicio.isoformat()}T{hora_inicio.strftime('%H:%M:%S')}-05:00"
                    datos["fecha_inicio_preparacion"] = inicio_iso

                if nuevo == "Atendido":
                    entrega_iso = f"{fecha_entrega.isoformat()}T{hora_entrega.strftime('%H:%M:%S')}-05:00"
                    inicio_dt = datetime.combine(fecha_inicio, hora_inicio)
                    entrega_dt = datetime.combine(fecha_entrega, hora_entrega)
                    if entrega_dt < inicio_dt:
                        st.error("La fecha y hora de entrega no pueden ser anteriores al inicio de preparación.")
                        st.stop()
                    datos["fecha_entrega"] = entrega_iso
                    datos["entrega_completa"] = entrega_completa

                try:
                    (
                        supabase.table("requerimientos")
                        .update(datos)
                        .eq("id", r["id"])
                        .execute()
                    )
                    st.session_state["flash"] = (
                        f'Requerimiento {r.get("numero_requerimiento") or ""} actualizado a {nuevo}.'
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudo actualizar el requerimiento: {e}")

# =========================================================
# UBICACIONES
# =========================================================
elif opcion == "📍  Ubicaciones":
    titulo_modulo("Ubicaciones de almacén")
    flash()
    st.caption("Consulta y actualiza la ubicación física registrada de los productos.")
    filas = []
    for p in productos_activos:
        filas.append({"ID": p.get("id"), "Modelo": p.get("modelo"), "Producto": p.get("producto"), "Marca": p.get("marca"), "Ubicación": p.get("ubicacion"), "Stock": p.get("stock_actual")})
    df = pd.DataFrame(filas)
    buscar = st.text_input("🔎 Buscar producto o ubicación")
    vista = df.copy()
    if buscar.strip() and not vista.empty:
        txt = vista.astype(str).agg(" ".join, axis=1)
        vista = vista[txt.str.contains(buscar.strip(), case=False, na=False)]
    st.dataframe(vista, use_container_width=True, hide_index=True, height=430)
    mostrar_descarga(vista, "ubicaciones_inventario.xlsx", "Ubicaciones")

    st.subheader("Actualizar ubicación")
    mapa = {etiqueta_producto(p): p for p in productos_activos}
    if mapa:
        elegido = st.selectbox("Producto", list(mapa.keys()))
        p = mapa[elegido]
        nueva = st.text_input("Nueva ubicación", value=p.get("ubicacion") or "")
        if st.button("💾 Guardar ubicación", use_container_width=True):
            if not nueva.strip():
                st.error("Ingrese una ubicación.")
            else:
                try:
                    supabase.table("productos").update({"ubicacion": nueva.strip()}).eq("id", p["id"]).execute()
                    st.session_state["flash"] = "Ubicación actualizada correctamente."
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudo actualizar la ubicación: {e}")

# =========================================================
# REPORTES OPERATIVOS
# =========================================================
elif opcion == "📈  Reportes":
    titulo_modulo("Reportes")
    st.caption("Información operativa obtenida de los registros del sistema.")
    movs = cargar_tabla("movimientos", "fecha_movimiento")
    reqs = cargar_tabla("requerimientos", "fecha_solicitud")
    t1, t2, t3, t4 = st.tabs(["📦 Inventario", "⬇️⬆️ Entradas y salidas", "🔄 Kardex", "📋 Requerimientos"])

    with t1:
        filas = []
        for p in productos_activos:
            stock = float(p.get("stock_actual") or 0); minimo = float(p.get("stock_minimo") or 0); maximo = float(p.get("stock_maximo") or 0)
            estado = "STOCK BAJO" if stock < minimo else ("SOBRESTOCK" if maximo > 0 and stock > maximo else "NORMAL")
            filas.append({"Modelo":p.get("modelo"),"Producto":p.get("producto"),"Marca":p.get("marca"),"Categoría":p.get("categoria"),"Stock actual":stock,"Stock mínimo":minimo,"Stock máximo":maximo,"Estado stock":estado,"Ubicación":p.get("ubicacion"),"Precio compra S/":float(p.get("precio_compra") or 0),"Valor inventario S/":stock*float(p.get("precio_compra") or 0)})
        dfi = pd.DataFrame(filas)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Productos activos", len(dfi)); c2.metric("Stock bajo", int((dfi["Estado stock"]=="STOCK BAJO").sum()) if not dfi.empty else 0); c3.metric("Sobrestock", int((dfi["Estado stock"]=="SOBRESTOCK").sum()) if not dfi.empty else 0); c4.metric("Valor inventario", f'S/ {dfi["Valor inventario S/"].sum():,.2f}' if not dfi.empty else "S/ 0.00")
        st.dataframe(dfi, use_container_width=True, hide_index=True, height=450)
        mostrar_descarga(dfi, "reporte_inventario.xlsx", "Inventario")

    with t2:
        if movs:
            dfm = pd.DataFrame(movs)
            nombres = {p["id"]: etiqueta_producto(p) for p in productos}
            if "producto_id" in dfm: dfm.insert(1,"Producto",dfm["producto_id"].map(nombres))
            st.dataframe(dfm, use_container_width=True, hide_index=True, height=450)
            mostrar_descarga(dfm, "reporte_entradas_salidas.xlsx", "Movimientos")
        else: st.info("Aún no existen entradas o salidas registradas.")

    with t3:
        if movs:
            dfk = pd.DataFrame(movs)
            nombres = {p["id"]: etiqueta_producto(p) for p in productos}
            if "producto_id" in dfk: dfk.insert(1,"Producto",dfk["producto_id"].map(nombres))
            st.dataframe(dfk, use_container_width=True, hide_index=True, height=450)
            mostrar_descarga(dfk, "reporte_kardex.xlsx", "Kardex")
        else: st.info("Aún no existen movimientos para el Kardex.")

    with t4:
        if reqs:
            dfr = pd.DataFrame(reqs)
            st.dataframe(dfr, use_container_width=True, hide_index=True, height=450)
            mostrar_descarga(dfr, "reporte_requerimientos.xlsx", "Requerimientos")
        else: st.info("Aún no existen requerimientos registrados.")
