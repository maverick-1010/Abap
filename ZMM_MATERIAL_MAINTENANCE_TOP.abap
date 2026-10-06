*&---------------------------------------------------------------------*
*& Include          ZMM_MATERIAL_MAINTENANCE_TOP
*&---------------------------------------------------------------------*
*& Mapping syntax in the view tables (BAPI_STRUCT_NAME / BAPI_FIELD_NAME)
*&
*&  Target BAPI: BAPI_MATERIAL_SAVEREPLICA (mass maintenance, TESTRUN)
*&
*&  BAPI_STRUCT_NAME = DDIC structure of the BAPI table parameter
*&                     (BAPIE1MARART, BAPIE1MARCRT, BAPIE1MVKERT ...),
*&                     the parameter name (CLIENTDATA, PLANTDATA ...) or
*&                     the corresponding BAPI_MARA / BAPI_MARC ... name
*&  BAPI_FIELD_NAME  = one or more targets, separated by ','
*&                     target = [STRUCTURE-]FIELD[;QUALIFIER=VALUE...]
*&
*&  Examples
*&   MEINS   BAPIE1MARART  BASE_UOM
*&   MEINS   BAPIE1MARART  BASE_UOM,BAPIE1MARMRT-ALT_UNIT;LINE=BASE
*&   BRGEW   BAPIE1MARMRT  GROSS_WT;LINE=BASE     (same UoM line as MEINS)
*&   VRKME   BAPIE1MVKERT  SALES_UNIT,BAPIE1MARMRT-ALT_UNIT;LINE=SALES
*&   UMREZ   BAPIE1MARMRT  NUMERATOR;LINE=SALES
*&   PO_TEXT BAPIE1MLTXRT  TEXT_LINE;TEXT_ID=BEST (fixed component value)
*&   CHAR_NAME_1  BAPI1003_ALLOC_VALUES_CHAR  CHARACT
*&   CHAR_VALUE_1 BAPI1003_ALLOC_VALUES_CHAR  VALUE_CHAR
*&        -> table parameters: fields ending with _<n> share line <n>
*&   CLASS_NAME   BAPI1003_KEY  CLASSNUM
*&   CLASS_TYPE   BAPI1003_KEY  CLASSTYPE
*&
*&  The material number (MATERIAL / MATERIAL_LONG) of every BAPI table
*&  line and all X-structures are filled by the program.
*&---------------------------------------------------------------------*
TABLES sscrfields.

*----------------------------------------------------------------------*
* Constants
*----------------------------------------------------------------------*
CONSTANTS:
  BEGIN OF gc_op,                             "ZTMM_MATMAS_MAST-OPERATION_ID
    create TYPE z_de_op_id VALUE 'C',
    update TYPE z_de_op_id VALUE 'U',
    extend TYPE z_de_op_id VALUE 'E',
  END OF gc_op,

  BEGIN OF gc_view,                           "view tables
    basic  TYPE char10 VALUE 'BASIC',
    class  TYPE char10 VALUE 'CLASS',
    purch  TYPE char10 VALUE 'PURCH',
    mrp    TYPE char10 VALUE 'MRP',
    plntst TYPE char10 VALUE 'PLNTST',
    sales  TYPE char10 VALUE 'SALES',
    val    TYPE char10 VALUE 'VAL',
  END OF gc_view,

  BEGIN OF gc_col,                            "template columns with fixed meaning
    action     TYPE fieldname VALUE 'ACTION',
    message    TYPE fieldname VALUE 'MESSAGE',
    profile    TYPE fieldname VALUE 'PROCESS_PROFILE',
    ref_matnr  TYPE fieldname VALUE 'REFERENCE_MATNR',
    ref_werks  TYPE fieldname VALUE 'REF_WERKS',
    ref_vkorg  TYPE fieldname VALUE 'REF_VKORG',
    ref_vtweg  TYPE fieldname VALUE 'REF_VTWEG',
    ref_ekorg  TYPE fieldname VALUE 'REF_EKORG',
    def_mode   TYPE fieldname VALUE 'DEFAULT_MODE',
    copy_basic TYPE fieldname VALUE 'COPY_BASIC',
    copy_purch TYPE fieldname VALUE 'COPY_PURCH',
    copy_mrp   TYPE fieldname VALUE 'COPY_MRP',
    copy_sales TYPE fieldname VALUE 'COPY_SALES',
    copy_acct  TYPE fieldname VALUE 'COPY_ACCOUNTING',
    matnr      TYPE fieldname VALUE 'MATNR',
    mtart      TYPE fieldname VALUE 'MTART',
    mbrsh      TYPE fieldname VALUE 'MBRSH',
    werks      TYPE fieldname VALUE 'WERKS',
    vkorg      TYPE fieldname VALUE 'VKORG',
    vtweg      TYPE fieldname VALUE 'VTWEG',
    prdha      TYPE fieldname VALUE 'PRDHA',
  END OF gc_col,

  gc_hdr_row        TYPE i         VALUE 1,          "header = technical names
  gc_data_row       TYPE i         VALUE 2,          "first data row
  gc_prodh_levels   TYPE i         VALUE 5,          "PRODH_LVL1..5 -> PRDHA
  gc_objtab_mara    TYPE tabelle   VALUE 'MARA',     "classification object table
  gc_def_classtype  TYPE klassenart VALUE '001',     "default class type
  "Conditional mandatory: check CONDMAT_FIELD only if SOURCE_FIELD is filled
  gc_cond_if_source TYPE abap_bool VALUE abap_true,
  "Test run + Create without MATNR: draw internal number to simulate?
  "(the number is lost after the rollback)
  gc_sim_int_num    TYPE abap_bool VALUE abap_false.

*----------------------------------------------------------------------*
* Types
*----------------------------------------------------------------------*
TYPES:
  tt_fieldname TYPE STANDARD TABLE OF fieldname WITH EMPTY KEY,
  tt_raw       TYPE STANDARD TABLE OF string_table WITH EMPTY KEY,  "file rows/columns

  "View table directory
  BEGIN OF ty_viewtab,
    view    TYPE char10,
    tabname TYPE tabname,
    active  TYPE abap_bool,
  END OF ty_viewtab,
  tt_viewtab TYPE STANDARD TABLE OF ty_viewtab WITH EMPTY KEY,

  "Mapping target (parsed from BAPI_STRUCT_NAME / BAPI_FIELD_NAME)
  BEGIN OF ty_fixed,
    comp  TYPE fieldname,
    value TYPE string,
  END OF ty_fixed,
  tt_fixed TYPE STANDARD TABLE OF ty_fixed WITH EMPTY KEY,

  BEGIN OF ty_target,
    param   TYPE fieldname,          "BAPI parameter, e.g. PLANTDATA
    comp    TYPE fieldname,          "component,      e.g. MRP_TYPE
    table   TYPE abap_bool,          "TABLES parameter
    linekey TYPE string,             "explicit line (LINE=...)
    fixed   TYPE tt_fixed,           "fixed component values
  END OF ty_target,
  tt_target TYPE STANDARD TABLE OF ty_target WITH EMPTY KEY.

"Field catalogue = view table line + view id + parsed targets
TYPES BEGIN OF ty_fcat.
INCLUDE TYPE ztmm_basic_data.
TYPES:
  view    TYPE char10,
  targets TYPE tt_target,
  END OF ty_fcat.

TYPES:
  tt_fcat TYPE STANDARD TABLE OF ty_fcat WITH EMPTY KEY
          WITH NON-UNIQUE SORTED KEY k_field COMPONENTS temp_field_name,
  tt_cond TYPE STANDARD TABLE OF ztmm_cond_mand WITH EMPTY KEY,

  "Template content (only non-empty cells)
  BEGIN OF ty_cell,
    row   TYPE i,
    field TYPE fieldname,
    value TYPE string,
  END OF ty_cell,
  tt_cell TYPE SORTED TABLE OF ty_cell WITH UNIQUE KEY row field,

  BEGIN OF ty_rowfield,
    row   TYPE i,
    field TYPE fieldname,
  END OF ty_rowfield,
  tt_rowfield TYPE SORTED TABLE OF ty_rowfield WITH UNIQUE KEY row field,

  "Template row
  BEGIN OF ty_row,
    row    TYPE i,
    matkey TYPE string,              "MATNR or '#<row>' (internal numbering)
    werks  TYPE werks_d,
    vkorg  TYPE vkorg,
    vtweg  TYPE vtweg,
  END OF ty_row,
  tt_row TYPE STANDARD TABLE OF ty_row WITH EMPTY KEY,

  "Log / ALV output
  BEGIN OF ty_msg,
    icon  TYPE icon_d,
    msgty TYPE symsgty,
    row   TYPE i,
    matnr TYPE char40,
    werks TYPE werks_d,
    vkorg TYPE vkorg,
    vtweg TYPE vtweg,
    view  TYPE char10,
    field TYPE fieldname,
    fdesc TYPE z_de_field_desc,
    text  TYPE bapi_msg,
  END OF ty_msg,
  tt_msg TYPE STANDARD TABLE OF ty_msg WITH EMPTY KEY,

  "Line index of table parameters (param + line key -> index)
  BEGIN OF ty_linekey,
    param TYPE fieldname,
    key   TYPE string,
    idx   TYPE i,
  END OF ty_linekey,
  tt_linekey TYPE STANDARD TABLE OF ty_linekey WITH EMPTY KEY,

  tt_views TYPE SORTED TABLE OF char10 WITH UNIQUE KEY table_line,

  "Template data of one row, mapped to the structures of
  "BAPI_MATERIAL_SAVEREPLICA (one line per org. level parameter).
  "Component names = BAPI parameter names (used dynamically!)
  BEGIN OF ty_bapi,
    headdata             TYPE bapie1mathead,
    clientdata           TYPE bapie1marart,
    plantdata            TYPE bapie1marcrt,
    forecastparameters   TYPE bapie1mpoprt,
    planningdata         TYPE bapie1mpgdrt,
    storagelocationdata  TYPE bapie1mardrt,
    valuationdata        TYPE bapie1mbewrt,
    warehousenumberdata  TYPE bapie1mlgnrt,
    salesdata            TYPE bapie1mvkert,
    storagetypedata      TYPE bapie1mlgtrt,
    materialdescription  TYPE STANDARD TABLE OF bapie1maktrt WITH EMPTY KEY,
    unitsofmeasure       TYPE STANDARD TABLE OF bapie1marmrt WITH EMPTY KEY,
    internationalartnos  TYPE STANDARD TABLE OF bapie1meanrt WITH EMPTY KEY,
    materiallongtext     TYPE STANDARD TABLE OF bapie1mltxrt WITH EMPTY KEY,
    taxclassifications   TYPE STANDARD TABLE OF bapie1mlanrt WITH EMPTY KEY,
    "classification (BAPI_OBJCL_*)
    classkey             TYPE bapi1003_key,
    allocvalueschar      TYPE STANDARD TABLE OF bapi1003_alloc_values_char WITH EMPTY KEY,
    allocvaluesnum       TYPE STANDARD TABLE OF bapi1003_alloc_values_num  WITH EMPTY KEY,
    allocvaluescurr      TYPE STANDARD TABLE OF bapi1003_alloc_values_curr WITH EMPTY KEY,
    "meta data
    row                  TYPE i,
    matkey               TYPE string,
    views                TYPE tt_views,           "views with data in this row
    line_keys            TYPE tt_linekey,
  END OF ty_bapi,
  tt_bapi TYPE STANDARD TABLE OF ty_bapi WITH EMPTY KEY,

  "Origin of a BAPI table line (for message -> template row)
  BEGIN OF ty_origin,
    param TYPE fieldname,
    idx   TYPE i,
    row   TYPE i,
  END OF ty_origin,
  tt_origin TYPE STANDARD TABLE OF ty_origin WITH EMPTY KEY,

  "One BAPI_MATERIAL_SAVEREPLICA call = one material, all org. levels.
  "Component names = TABLES parameter names of the BAPI
  BEGIN OF ty_call,
    headdata             TYPE STANDARD TABLE OF bapie1mathead  WITH EMPTY KEY,
    clientdata           TYPE STANDARD TABLE OF bapie1marart   WITH EMPTY KEY,
    clientdatax          TYPE STANDARD TABLE OF bapie1marartx  WITH EMPTY KEY,
    plantdata            TYPE STANDARD TABLE OF bapie1marcrt   WITH EMPTY KEY,
    plantdatax           TYPE STANDARD TABLE OF bapie1marcrtx  WITH EMPTY KEY,
    forecastparameters   TYPE STANDARD TABLE OF bapie1mpoprt   WITH EMPTY KEY,
    forecastparametersx  TYPE STANDARD TABLE OF bapie1mpoprtx  WITH EMPTY KEY,
    planningdata         TYPE STANDARD TABLE OF bapie1mpgdrt   WITH EMPTY KEY,
    planningdatax        TYPE STANDARD TABLE OF bapie1mpgdrtx  WITH EMPTY KEY,
    storagelocationdata  TYPE STANDARD TABLE OF bapie1mardrt   WITH EMPTY KEY,
    storagelocationdatax TYPE STANDARD TABLE OF bapie1mardrtx  WITH EMPTY KEY,
    valuationdata        TYPE STANDARD TABLE OF bapie1mbewrt   WITH EMPTY KEY,
    valuationdatax       TYPE STANDARD TABLE OF bapie1mbewrtx  WITH EMPTY KEY,
    warehousenumberdata  TYPE STANDARD TABLE OF bapie1mlgnrt   WITH EMPTY KEY,
    warehousenumberdatax TYPE STANDARD TABLE OF bapie1mlgnrtx  WITH EMPTY KEY,
    salesdata            TYPE STANDARD TABLE OF bapie1mvkert   WITH EMPTY KEY,
    salesdatax           TYPE STANDARD TABLE OF bapie1mvkertx  WITH EMPTY KEY,
    storagetypedata      TYPE STANDARD TABLE OF bapie1mlgtrt   WITH EMPTY KEY,
    storagetypedatax     TYPE STANDARD TABLE OF bapie1mlgtrtx  WITH EMPTY KEY,
    materialdescription  TYPE STANDARD TABLE OF bapie1maktrt   WITH EMPTY KEY,
    unitsofmeasure       TYPE STANDARD TABLE OF bapie1marmrt   WITH EMPTY KEY,
    unitsofmeasurex      TYPE STANDARD TABLE OF bapie1marmrtx  WITH EMPTY KEY,
    internationalartnos  TYPE STANDARD TABLE OF bapie1meanrt   WITH EMPTY KEY,
    materiallongtext     TYPE STANDARD TABLE OF bapie1mltxrt   WITH EMPTY KEY,
    taxclassifications   TYPE STANDARD TABLE OF bapie1mlanrt   WITH EMPTY KEY,
    origin               TYPE tt_origin,
  END OF ty_call,

  "Reference material cache
  BEGIN OF ty_refcache,
    key  TYPE string,
    data TYPE ty_bapi,
  END OF ty_refcache,
  tt_refcache TYPE STANDARD TABLE OF ty_refcache WITH EMPTY KEY.
