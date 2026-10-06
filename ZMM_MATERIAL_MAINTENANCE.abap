*&---------------------------------------------------------------------*
*& Report ZMM_MATERIAL_MAINTENANCE
*&---------------------------------------------------------------------*
*& Material master Create / Update / Extend from an upload template
*&
*&  - Template: .xlsx or .csv, local PC or application server (AL11)
*&  - Active variant from ZTMM_MATMAS_MAST (type/sector/profile/action)
*&  - Field catalogue per view from the view tables
*&      ZTMM_BASIC_DATA  (Basic data)        <- P_GEN
*&      ZTMM_CLASS_DATA  (Classification)    <- P_CLASS
*&      ZTMM_PURCH_DATA  (Purchasing)        <- P_PURS
*&      ZTMM_MRP_DATA    (MRP)               <- P_MRP
*&      ZTMM_PLNTST_DATA (Plant data/storage)<- P_STORE
*&      ZTMM_SALES_DATA  (Sales org / distr.)<- P_SALES
*&      ZTMM_VAL_DATA    (Valuation)         <- P_ACCT
*&  - Mandatory / optional / system-derived / conditional-mandatory
*&    validation (ZTMM_COND_MAND)
*&  - Fully dynamic mapping template field -> BAPI structure-field
*&    (BAPI_STRUCT_NAME / BAPI_FIELD_NAME) - no code change needed
*&    for new fields
*&  - P_TEST = 'X': simulation - BAPI_MATERIAL_SAVEREPLICA with TESTRUN
*&    P_TEST = ' ': posting    - BAPI_MATERIAL_SAVEREPLICA + commit
*&      one call per template row: basic data of the material + the
*&      org. levels of that row (plant, sales area, valuation area ...)
*&      BAPI_OBJCL_CREATE / BAPI_OBJCL_CHANGE (classification)
*&  - Create : material must not exist, all supplied views are created
*&    Update : material + org. levels must exist; template is compared
*&             with the current data, only changed fields are sent and
*&             every change is logged (old -> new)
*&    Extend : material must exist; only org. levels that do not exist
*&             yet are created, basic data / existing levels unchanged
*&  - Output log as ALV, stored on the application server (XLSX)
*&    and sent by e-mail
*&  - Pushbutton: download of the upload template as .xlsx (sheet
*&    TEMPLATE + sheet FIELD_INFO with the flags of the active variant)
*&
*& Includes
*&   ZMM_MATERIAL_MAINTENANCE_TOP  global types / constants
*&   ZMM_MATERIAL_MAINTENANCE_S01  selection screen
*&   ZMM_MATERIAL_MAINTENANCE_C01  class definitions
*&   ZMM_MATERIAL_MAINTENANCE_C02  class implementations (part 1)
*&   ZMM_MATERIAL_MAINTENANCE_C03  class implementations (part 2)
*&---------------------------------------------------------------------*
REPORT zmm_material_maintenance.

INCLUDE zmm_material_maintenance_top.
INCLUDE zmm_material_maintenance_s01.
INCLUDE zmm_material_maintenance_c01.
INCLUDE zmm_material_maintenance_c02.
INCLUDE zmm_material_maintenance_c03.

*----------------------------------------------------------------------*
INITIALIZATION.
  lcl_screen=>initialization( ).

AT SELECTION-SCREEN OUTPUT.
  lcl_screen=>pbo( ).

AT SELECTION-SCREEN ON VALUE-REQUEST FOR p_file1.
  lcl_screen=>f4_local_file( CHANGING cv_file = p_file1 ).

AT SELECTION-SCREEN.
  lcl_screen=>pai( ).

START-OF-SELECTION.
  NEW lcl_app( )->run( ).
