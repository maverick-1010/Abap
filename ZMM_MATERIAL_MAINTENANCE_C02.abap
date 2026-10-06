*&---------------------------------------------------------------------*
*& Include          ZMM_MATERIAL_MAINTENANCE_C02
*&---------------------------------------------------------------------*
*& Class implementations - part 1
*&   lcx_error, lcl_log, lcl_mapper, lcl_file_reader, lcl_config,
*&   lcl_material_bapi
*& (part 2 in ZMM_MATERIAL_MAINTENANCE_C03)
*&---------------------------------------------------------------------*

CLASS lcx_error IMPLEMENTATION.
  METHOD constructor.
    super->constructor( ).
    mv_text = iv_text.
  ENDMETHOD.
  METHOD get_text.
    result = mv_text.
  ENDMETHOD.
ENDCLASS.

*======================================================================*
* LCL_LOG
*======================================================================*
CLASS lcl_log IMPLEMENTATION.

  METHOD add.
    DATA(ls_msg) = VALUE ty_msg(
      icon  = SWITCH #( iv_type WHEN 'E' OR 'A' THEN icon_red_light
                                WHEN 'W'        THEN icon_yellow_light
                                ELSE                 icon_green_light )
      msgty = COND #( WHEN iv_type = 'A' THEN 'E' ELSE iv_type )
      row   = is_row-row
      werks = is_row-werks
      vkorg = is_row-vkorg
      vtweg = is_row-vtweg
      view  = iv_view
      field = iv_field
      fdesc = iv_fdesc
      text  = iv_text ).

    ls_msg-matnr = COND #( WHEN iv_matnr IS NOT INITIAL THEN iv_matnr
                           WHEN lcl_mapper=>is_dummy_key( is_row-matkey ) = abap_false
                           THEN is_row-matkey ).

    "no duplicates (same field can be maintained in several view tables)
    IF line_exists( mt_msg[ row   = ls_msg-row   msgty = ls_msg-msgty
                            field = ls_msg-field text  = ls_msg-text ] ).
      RETURN.
    ENDIF.
    APPEND ls_msg TO mt_msg.
  ENDMETHOD.

  METHOD count.
    rv_count = REDUCE i( INIT n = 0
                         FOR ls_msg IN mt_msg WHERE ( msgty = iv_type )
                         NEXT n = n + 1 ).
  ENDMETHOD.

  METHOD has_error.
    rv_error = COND #( WHEN line_exists( mt_msg[ row = iv_row msgty = 'E' ] )
                       THEN abap_true ELSE abap_false ).
  ENDMETHOD.

  METHOD has_global_error.
    rv_error = COND #( WHEN line_exists( mt_msg[ row = 0 msgty = 'E' ] )
                       THEN abap_true ELSE abap_false ).
  ENDMETHOD.

ENDCLASS.

*======================================================================*
* LCL_MAPPER - generic, field-symbol based mapping
*======================================================================*
CLASS lcl_mapper IMPLEMENTATION.

  METHOD trim.
    rv_value = iv_value.
    rv_value = replace( val = rv_value regex = `^\s+|\s+$` with = `` occ = 0 ).
  ENDMETHOD.

  METHOD is_dummy_key.
    IF iv_key IS INITIAL.
      rv_dummy = abap_true.
      RETURN.
    ENDIF.
    rv_dummy = COND #( WHEN iv_key(1) = '#' THEN abap_true ELSE abap_false ).
  ENDMETHOD.

  METHOD resolve_param.
    "DDIC structure name -> parameter of BAPI_MATERIAL_SAVEREPLICA
    "(BAPIE1* structures; the BAPI_MARA ... names are accepted as well,
    " their field names are identical)
    CONSTANTS lc_tables TYPE string VALUE
      ` MATERIALDESCRIPTION UNITSOFMEASURE INTERNATIONALARTNOS MATERIALLONGTEXT TAXCLASSIFICATIONS ALLOCVALUESCHAR ALLOCVALUESNUM ALLOCVALUESCURR `.
    CONSTANTS lc_single TYPE string VALUE
      ` HEADDATA CLIENTDATA PLANTDATA FORECASTPARAMETERS PLANNINGDATA STORAGELOCATIONDATA VALUATIONDATA WAREHOUSENUMBERDATA SALESDATA STORAGETYPEDATA CLASSKEY `.

    CLEAR: ev_param, ev_table.
    DATA(lv_struct) = to_upper( trim( iv_struct ) ).

    ev_param = SWITCH fieldname( lv_struct
                 WHEN 'BAPIE1MATHEAD'              THEN 'HEADDATA'       "SAVEREPLICA
                 WHEN 'BAPIE1MARART'               THEN 'CLIENTDATA'
                 WHEN 'BAPIE1MARCRT'               THEN 'PLANTDATA'
                 WHEN 'BAPIE1MPOPRT'               THEN 'FORECASTPARAMETERS'
                 WHEN 'BAPIE1MPGDRT'               THEN 'PLANNINGDATA'
                 WHEN 'BAPIE1MARDRT'               THEN 'STORAGELOCATIONDATA'
                 WHEN 'BAPIE1MBEWRT'               THEN 'VALUATIONDATA'
                 WHEN 'BAPIE1MLGNRT'               THEN 'WAREHOUSENUMBERDATA'
                 WHEN 'BAPIE1MVKERT'               THEN 'SALESDATA'
                 WHEN 'BAPIE1MLGTRT'               THEN 'STORAGETYPEDATA'
                 WHEN 'BAPIE1MAKTRT'               THEN 'MATERIALDESCRIPTION'
                 WHEN 'BAPIE1MARMRT'               THEN 'UNITSOFMEASURE'
                 WHEN 'BAPIE1MEANRT'               THEN 'INTERNATIONALARTNOS'
                 WHEN 'BAPIE1MLTXRT'               THEN 'MATERIALLONGTEXT'
                 WHEN 'BAPIE1MLANRT'               THEN 'TAXCLASSIFICATIONS'
                 WHEN 'BAPIMATHEAD'                THEN 'HEADDATA'       "SAVEDATA names
                 WHEN 'BAPI_MARA'                  THEN 'CLIENTDATA'
                 WHEN 'BAPI_MARC'                  THEN 'PLANTDATA'
                 WHEN 'BAPI_MPOP'                  THEN 'FORECASTPARAMETERS'
                 WHEN 'BAPI_MPGD'                  THEN 'PLANNINGDATA'
                 WHEN 'BAPI_MARD'                  THEN 'STORAGELOCATIONDATA'
                 WHEN 'BAPI_MBEW'                  THEN 'VALUATIONDATA'
                 WHEN 'BAPI_MLGN'                  THEN 'WAREHOUSENUMBERDATA'
                 WHEN 'BAPI_MVKE'                  THEN 'SALESDATA'
                 WHEN 'BAPI_MLGT'                  THEN 'STORAGETYPEDATA'
                 WHEN 'BAPI_MAKT'                  THEN 'MATERIALDESCRIPTION'
                 WHEN 'BAPI_MARM'                  THEN 'UNITSOFMEASURE'
                 WHEN 'BAPI_MEAN'                  THEN 'INTERNATIONALARTNOS'
                 WHEN 'BAPI_MLTX'                  THEN 'MATERIALLONGTEXT'
                 WHEN 'BAPI_MLAN'                  THEN 'TAXCLASSIFICATIONS'
                 WHEN 'BAPI1003_KEY'               THEN 'CLASSKEY'
                 WHEN 'BAPI1003_ALLOC_VALUES_CHAR' THEN 'ALLOCVALUESCHAR'
                 WHEN 'BAPI1003_ALLOC_VALUES_NUM'  THEN 'ALLOCVALUESNUM'
                 WHEN 'BAPI1003_ALLOC_VALUES_CURR' THEN 'ALLOCVALUESCURR'
                 ELSE lv_struct ).                    "parameter name given directly

    IF lc_tables CS | { ev_param } |.
      ev_table = abap_true.
    ELSEIF lc_single NS | { ev_param } |.
      CLEAR ev_param.                                 "not supported
    ENDIF.
  ENDMETHOD.

  METHOD target_exists.
    FIELD-SYMBOLS: <lt_tab> TYPE STANDARD TABLE,
                   <ls_str> TYPE any,
                   <lv_cmp> TYPE any.
    DATA ls_probe TYPE ty_bapi.

    IF is_target-table = abap_true.
      ASSIGN COMPONENT is_target-param OF STRUCTURE ls_probe TO <lt_tab>.
      CHECK sy-subrc = 0.
      APPEND INITIAL LINE TO <lt_tab> ASSIGNING <ls_str>.
    ELSE.
      ASSIGN COMPONENT is_target-param OF STRUCTURE ls_probe TO <ls_str>.
      CHECK sy-subrc = 0.
    ENDIF.

    ASSIGN COMPONENT is_target-comp OF STRUCTURE <ls_str> TO <lv_cmp>.
    CHECK sy-subrc = 0.
    LOOP AT is_target-fixed INTO DATA(ls_fixed).
      ASSIGN COMPONENT ls_fixed-comp OF STRUCTURE <ls_str> TO <lv_cmp>.
      CHECK sy-subrc <> 0.
      RETURN.                                         "fixed component unknown
    ENDLOOP.
    rv_exists = abap_true.
  ENDMETHOD.

  METHOD get_line.
    "Line of a TABLES parameter identified by a line key
    FIELD-SYMBOLS: <lt_tab>  TYPE STANDARD TABLE,
                   <ls_line> TYPE any.

    CLEAR er_line.
    ASSIGN COMPONENT iv_param OF STRUCTURE cs_bapi TO <lt_tab>.
    CHECK sy-subrc = 0.

    READ TABLE cs_bapi-line_keys INTO DATA(ls_key)
         WITH KEY param = iv_param key = iv_key.
    IF sy-subrc = 0.
      READ TABLE <lt_tab> ASSIGNING <ls_line> INDEX ls_key-idx.
    ELSE.
      APPEND INITIAL LINE TO <lt_tab> ASSIGNING <ls_line>.
      APPEND VALUE #( param = iv_param key = iv_key idx = lines( <lt_tab> ) )
        TO cs_bapi-line_keys.
    ENDIF.
    er_line = REF #( <ls_line> ).
  ENDMETHOD.

  METHOD map_value.
    FIELD-SYMBOLS: <ls_tgt> TYPE any,
                   <lv_tgt> TYPE any,
                   <lv_fix> TYPE any.
    DATA: lv_suffix TYPE string,
          lv_key    TYPE string,
          lr_line   TYPE REF TO data,
          lv_value  TYPE string,
          lv_rest   TYPE string.

    CLEAR ev_error.
    lv_value = iv_value.

    "--- target structure (single parameter or line of a table parameter)
    IF is_target-table = abap_true.
      lv_key = is_target-linekey.
      IF lv_key IS INITIAL.
        "fields ending with _<n> (CHAR_NAME_1 / CHAR_VALUE_1) share line <n>
        FIND REGEX `_(\d+)$` IN iv_field SUBMATCHES lv_suffix.
        lv_key = |{ REDUCE string( INIT k = `` FOR f IN is_target-fixed
                                   NEXT k = |{ k }{ f-comp }={ f-value };| ) }| &&
                 |#{ COND string( WHEN lv_suffix IS INITIAL THEN `1` ELSE lv_suffix ) }|.
      ENDIF.
      get_line( EXPORTING iv_param = is_target-param
                          iv_key   = lv_key
                IMPORTING er_line  = lr_line
                CHANGING  cs_bapi  = cs_bapi ).
      IF lr_line IS BOUND.
        ASSIGN lr_line->* TO <ls_tgt>.
      ENDIF.
    ELSE.
      ASSIGN COMPONENT is_target-param OF STRUCTURE cs_bapi TO <ls_tgt>.
    ENDIF.

    IF <ls_tgt> IS NOT ASSIGNED.
      ev_error = |BAPI parameter { is_target-param } not available|.
      RETURN.
    ENDIF.

    "--- fixed component values (e.g. TEXT_ID=BEST)
    LOOP AT is_target-fixed INTO DATA(ls_fixed).
      ASSIGN COMPONENT ls_fixed-comp OF STRUCTURE <ls_tgt> TO <lv_fix>.
      IF sy-subrc = 0.
        <lv_fix> = ls_fixed-value.
      ENDIF.
    ENDLOOP.

    "--- target field
    ASSIGN COMPONENT is_target-comp OF STRUCTURE <ls_tgt> TO <lv_tgt>.
    IF sy-subrc <> 0.
      ev_error = |Field { is_target-param }-{ is_target-comp } does not exist|.
      RETURN.
    ENDIF.

    "Long texts longer than one line (132 char) -> continuation lines
    IF is_target-param = 'MATERIALLONGTEXT' AND is_target-comp = 'TEXT_LINE' AND
       strlen( lv_value ) > 132.
      lv_rest  = substring( val = lv_value off = 132 ).
      lv_value = substring( val = lv_value len = 132 ).
    ENDIF.

    move_value( EXPORTING iv_value  = lv_value
                IMPORTING ev_error  = ev_error
                CHANGING  cv_target = <lv_tgt> ).

    IF lv_rest IS NOT INITIAL AND ev_error IS INITIAL.
      DATA(ls_text) = CONV bapie1mltxrt( <ls_tgt> ).
      WHILE lv_rest IS NOT INITIAL.
        ls_text-text_line = lv_rest.
        APPEND ls_text TO cs_bapi-materiallongtext.
        lv_rest = COND #( WHEN strlen( lv_rest ) > 132
                          THEN substring( val = lv_rest off = 132 ) ELSE `` ).
      ENDWHILE.
    ENDIF.
  ENDMETHOD.

  METHOD move_value.
    "Type-driven conversion of a template value into a BAPI field
    DATA: ls_dfies TYPE dfies,
          lv_date  TYPE d,
          lv_fm    TYPE rs38l_fnam.

    CLEAR ev_error.
    DATA(lo_elem)  = CAST cl_abap_elemdescr( cl_abap_typedescr=>describe_by_data( cv_target ) ).
    DATA(lv_value) = iv_value.

    TRY.
        CASE lo_elem->type_kind.

          WHEN cl_abap_typedescr=>typekind_string.
            cv_target = lv_value.

          WHEN cl_abap_typedescr=>typekind_date.
            IF lv_value CO '0123456789' AND strlen( lv_value ) <= 5.
              lv_date = '18991230'.                       "Excel serial date
              lv_date = lv_date + CONV i( lv_value ).
            ELSEIF lv_value CO '0123456789' AND strlen( lv_value ) = 8.
              lv_date = lv_value.                         "YYYYMMDD
            ELSE.
              CALL FUNCTION 'CONVERT_DATE_TO_INTERNAL'   "user format
                EXPORTING  date_external = lv_value
                IMPORTING  date_internal = lv_date
                EXCEPTIONS OTHERS        = 1.
              IF sy-subrc <> 0.
                CLEAR lv_date.
              ENDIF.
            ENDIF.
            IF lv_date IS INITIAL OR CONV i( lv_date ) = 0.
              ev_error = |Invalid date '{ lv_value }'|.
              RETURN.
            ENDIF.
            cv_target = lv_date.

          WHEN cl_abap_typedescr=>typekind_packed OR cl_abap_typedescr=>typekind_int
            OR cl_abap_typedescr=>typekind_int1   OR cl_abap_typedescr=>typekind_int2
            OR cl_abap_typedescr=>typekind_float
            OR cl_abap_typedescr=>typekind_decfloat16
            OR cl_abap_typedescr=>typekind_decfloat34.
            CONDENSE lv_value NO-GAPS.
            IF lv_value CS '.'.
              REPLACE ALL OCCURRENCES OF ',' IN lv_value WITH ''.   "1,234.50
            ELSE.
              REPLACE ALL OCCURRENCES OF ',' IN lv_value WITH '.'.  "12,5
            ENDIF.
            cv_target = lv_value.                         "raises on bad format

          WHEN cl_abap_typedescr=>typekind_char OR cl_abap_typedescr=>typekind_num.
            IF lo_elem->is_ddic_type( ) = abap_true.
              lo_elem->get_ddic_field( RECEIVING p_flddescr = ls_dfies EXCEPTIONS OTHERS = 1 ).
            ENDIF.

            IF ls_dfies-convexit IS NOT INITIAL.          "ALPHA, MATN1, CUNIT, ISOLA ...
              lv_fm = |CONVERSION_EXIT_{ ls_dfies-convexit }_INPUT|.
              CALL FUNCTION lv_fm
                EXPORTING  input         = lv_value
                IMPORTING  output        = cv_target
                EXCEPTIONS error_message = 1
                           OTHERS        = 2.
              IF sy-subrc <> 0.
                CLEAR cv_target.
                ev_error = |Value '{ lv_value }' rejected by conversion exit { ls_dfies-convexit }|.
              ENDIF.
              RETURN.
            ENDIF.

            DATA(lv_maxlen) = lo_elem->length / cl_abap_char_utilities=>charsize.
            IF strlen( lv_value ) > lv_maxlen.
              ev_error = |Value '{ lv_value }' exceeds maximum length { lv_maxlen }|.
              RETURN.
            ENDIF.
            IF lo_elem->type_kind = cl_abap_typedescr=>typekind_num AND lv_value CN '0123456789'.
              ev_error = |Value '{ lv_value }' must be numeric|.
              RETURN.
            ENDIF.
            cv_target = lv_value.

          WHEN OTHERS.
            cv_target = lv_value.
        ENDCASE.

      CATCH cx_sy_conversion_error cx_sy_dyn_call_error INTO DATA(lx_conv).
        CLEAR cv_target.
        ev_error = |Invalid value '{ lv_value }': { lx_conv->get_text( ) }|.
    ENDTRY.
  ENDMETHOD.

  METHOD set_x.
    "Same type as data field -> key field (PLANT, SALES_ORG ...): copy value
    "otherwise BAPIUPDATE flag
    IF cl_abap_typedescr=>describe_by_data( cv_x )->absolute_name =
       cl_abap_typedescr=>describe_by_data( iv_value )->absolute_name.
      cv_x = iv_value.
    ELSE.
      cv_x = abap_true.
    ENDIF.
  ENDMETHOD.

  METHOD set_all_x.
    "Build X-structure from all filled components of the data structure
    FIELD-SYMBOLS: <lv_data> TYPE any,
                   <lv_x>    TYPE any.
    DATA(lo_x) = CAST cl_abap_structdescr( cl_abap_typedescr=>describe_by_data( cs_x ) ).
    LOOP AT lo_x->components INTO DATA(ls_comp).
      ASSIGN COMPONENT ls_comp-name OF STRUCTURE is_data TO <lv_data>.
      CHECK sy-subrc = 0.
      CHECK <lv_data> IS NOT INITIAL.
      ASSIGN COMPONENT ls_comp-name OF STRUCTURE cs_x TO <lv_x>.
      CHECK sy-subrc = 0.
      set_x( EXPORTING iv_value = <lv_data> CHANGING cv_x = <lv_x> ).
    ENDLOOP.
  ENDMETHOD.

  METHOD merge_struct.
    "Copy all non-initial components of IS_SRC into CS_TGT
    FIELD-SYMBOLS: <lv_src> TYPE any,
                   <lv_tgt> TYPE any.
    DO.
      ASSIGN COMPONENT sy-index OF STRUCTURE is_src TO <lv_src>.
      IF sy-subrc <> 0.
        EXIT.
      ENDIF.
      CHECK <lv_src> IS NOT INITIAL.
      ASSIGN COMPONENT sy-index OF STRUCTURE cs_tgt TO <lv_tgt>.
      IF sy-subrc = 0.
        <lv_tgt> = <lv_src>.
      ENDIF.
    ENDDO.
  ENDMETHOD.

  METHOD append_unique.
    FIELD-SYMBOLS <ls_line> TYPE any.
    LOOP AT ct_tab ASSIGNING <ls_line>.
      IF <ls_line> = is_line.
        RETURN.
      ENDIF.
    ENDLOOP.
    APPEND is_line TO ct_tab.
  ENDMETHOD.

  METHOD add_line.
    "Add a line to a TABLES parameter of the BAPI call. Lines with the
    "same org. key (e.g. PLANT) are merged, others are appended.
    FIELD-SYMBOLS: <lt_tab>  TYPE STANDARD TABLE,
                   <ls_line> TYPE any,
                   <lv_new>  TYPE any,
                   <lv_old>  TYPE any.
    DATA: lt_keys TYPE string_table,
          lv_same TYPE abap_bool.

    ASSIGN COMPONENT iv_param OF STRUCTURE cs_call TO <lt_tab>.
    CHECK sy-subrc = 0.

    DATA(lv_keys) = SWITCH string( iv_param
      WHEN 'CLIENTDATA'          THEN ``                          "one line per material
      WHEN 'PLANTDATA'           THEN `PLANT`
      WHEN 'FORECASTPARAMETERS'  THEN `PLANT`
      WHEN 'PLANNINGDATA'        THEN `PLANT`
      WHEN 'STORAGELOCATIONDATA' THEN `PLANT STGE_LOC`
      WHEN 'VALUATIONDATA'       THEN `VAL_AREA VAL_TYPE`
      WHEN 'WAREHOUSENUMBERDATA' THEN `WHSE_NO`
      WHEN 'SALESDATA'           THEN `SALES_ORG DISTR_CHAN`
      WHEN 'STORAGETYPEDATA'     THEN `WHSE_NO STGE_TYPE`
      WHEN 'MATERIALDESCRIPTION' THEN `LANGU LANGU_ISO`
      WHEN 'UNITSOFMEASURE'      THEN `ALT_UNIT ALT_UNIT_ISO`
      WHEN 'TAXCLASSIFICATIONS'  THEN `DEPCOUNTRY DEPCOUNTRY_ISO`
      WHEN 'INTERNATIONALARTNOS' THEN `UNIT UNIT_ISO EAN_UPC`
      ELSE `*` ).                                                "append (long texts)

    IF lv_keys = `*`.
      append_unique( EXPORTING is_line = is_line CHANGING ct_tab = <lt_tab> ).
      APPEND VALUE #( param = iv_param idx = lines( <lt_tab> ) row = iv_row ) TO cs_call-origin.
      RETURN.
    ENDIF.

    SPLIT lv_keys AT space INTO TABLE lt_keys.
    LOOP AT <lt_tab> ASSIGNING <ls_line>.
      DATA(lv_idx) = sy-tabix.
      lv_same = abap_true.
      LOOP AT lt_keys INTO DATA(lv_key) WHERE table_line IS NOT INITIAL.
        ASSIGN COMPONENT lv_key OF STRUCTURE is_line TO <lv_new>.
        CHECK sy-subrc = 0.
        ASSIGN COMPONENT lv_key OF STRUCTURE <ls_line> TO <lv_old>.
        CHECK sy-subrc = 0.
        IF <lv_new> <> <lv_old>.
          lv_same = abap_false.
          EXIT.
        ENDIF.
      ENDLOOP.
      IF lv_same = abap_true.
        merge_struct( EXPORTING is_src = is_line CHANGING cs_tgt = <ls_line> ).
        APPEND VALUE #( param = iv_param idx = lv_idx row = iv_row ) TO cs_call-origin.
        RETURN.
      ENDIF.
    ENDLOOP.

    APPEND is_line TO <lt_tab>.
    APPEND VALUE #( param = iv_param idx = lines( <lt_tab> ) row = iv_row ) TO cs_call-origin.
  ENDMETHOD.

  METHOD set_matnr.
    "MATERIAL (18) and - on S/4HANA - MATERIAL_LONG (40)
    FIELD-SYMBOLS: <lv_short> TYPE any,
                   <lv_long>  TYPE any.
    ASSIGN COMPONENT 'MATERIAL'      OF STRUCTURE cs_line TO <lv_short>.
    ASSIGN COMPONENT 'MATERIAL_LONG' OF STRUCTURE cs_line TO <lv_long>.
    IF <lv_long> IS ASSIGNED.
      <lv_long> = iv_matnr.
      IF <lv_short> IS ASSIGNED.
        IF strlen( iv_matnr ) <= 18.
          <lv_short> = iv_matnr.
        ELSE.
          CLEAR <lv_short>.
        ENDIF.
      ENDIF.
    ELSEIF <lv_short> IS ASSIGNED.
      <lv_short> = iv_matnr.
    ENDIF.
  ENDMETHOD.

  METHOD set_material_all.
    "Material number in every line of every TABLES parameter
    FIELD-SYMBOLS: <lt_tab>  TYPE STANDARD TABLE,
                   <ls_line> TYPE any.
    DATA(lo_call) = CAST cl_abap_structdescr( cl_abap_typedescr=>describe_by_data( cs_call ) ).
    LOOP AT lo_call->components INTO DATA(ls_comp) WHERE type_kind = cl_abap_typedescr=>typekind_table.
      CHECK ls_comp-name <> 'ORIGIN'.
      ASSIGN COMPONENT ls_comp-name OF STRUCTURE cs_call TO <lt_tab>.
      CHECK sy-subrc = 0.
      LOOP AT <lt_tab> ASSIGNING <ls_line>.
        set_matnr( EXPORTING iv_matnr = iv_matnr CHANGING cs_line = <ls_line> ).
      ENDLOOP.
    ENDLOOP.
  ENDMETHOD.

  METHOD build_x_tables.
    "For each parameter with an X counterpart (PLANTDATA -> PLANTDATAX ...)
    "one X line per data line: key fields copied, other filled fields = 'X'
    FIELD-SYMBOLS: <lt_data> TYPE STANDARD TABLE,
                   <lt_x>    TYPE STANDARD TABLE,
                   <ls_data> TYPE any,
                   <ls_x>    TYPE any.
    DATA(lo_call) = CAST cl_abap_structdescr( cl_abap_typedescr=>describe_by_data( cs_call ) ).
    LOOP AT lo_call->components INTO DATA(ls_comp) WHERE type_kind = cl_abap_typedescr=>typekind_table.
      DATA(lv_xname) = |{ ls_comp-name }X|.
      ASSIGN COMPONENT lv_xname OF STRUCTURE cs_call TO <lt_x>.
      CHECK sy-subrc = 0.
      ASSIGN COMPONENT ls_comp-name OF STRUCTURE cs_call TO <lt_data>.
      CHECK sy-subrc = 0.
      CLEAR <lt_x>.
      LOOP AT <lt_data> ASSIGNING <ls_data>.
        APPEND INITIAL LINE TO <lt_x> ASSIGNING <ls_x>.
        set_all_x( EXPORTING is_data = <ls_data> CHANGING cs_x = <ls_x> ).
      ENDLOOP.
    ENDLOOP.
  ENDMETHOD.

  METHOD set_default.
    "Set component if it exists and is still initial
    FIELD-SYMBOLS <lv_comp> TYPE any.
    ASSIGN COMPONENT iv_comp OF STRUCTURE cs_line TO <lv_comp>.
    IF sy-subrc = 0 AND <lv_comp> IS INITIAL.
      <lv_comp> = iv_value.
    ENDIF.
  ENDMETHOD.

  METHOD has_payload.
    "Call contains data besides the header (otherwise nothing to post)
    FIELD-SYMBOLS <lt_tab> TYPE STANDARD TABLE.
    DATA(lo_call) = CAST cl_abap_structdescr( cl_abap_typedescr=>describe_by_data( is_call ) ).
    LOOP AT lo_call->components INTO DATA(ls_comp) WHERE type_kind = cl_abap_typedescr=>typekind_table.
      CHECK ls_comp-name <> 'HEADDATA' AND ls_comp-name <> 'ORIGIN' AND ls_comp-name NP '*X'.
      ASSIGN COMPONENT ls_comp-name OF STRUCTURE is_call TO <lt_tab>.
      IF sy-subrc = 0 AND <lt_tab> IS NOT INITIAL.
        rv_payload = abap_true.
        RETURN.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.

*======================================================================*
* LCL_FILE_READER - .xlsx / .csv
*======================================================================*
CLASS lcl_file_reader IMPLEMENTATION.

  METHOD get_extension.
    DATA(lv_file) = to_lower( iv_file ).
    FIND REGEX `\.([a-z0-9]+)$` IN lv_file SUBMATCHES rv_ext.
  ENDMETHOD.

  METHOD read.
    CASE get_extension( iv_file ).
      WHEN 'xlsx'.
        rt_raw = parse_xlsx( iv_xdata = read_binary( iv_file = iv_file iv_server = iv_server )
                             iv_file  = iv_file ).
      WHEN 'csv'.
        rt_raw = parse_csv( read_text_lines( iv_file = iv_file iv_server = iv_server ) ).
      WHEN OTHERS.
        RAISE EXCEPTION TYPE lcx_error
          EXPORTING iv_text = |File { iv_file } not supported - only .xlsx and .csv files are allowed|.
    ENDCASE.

    IF lines( rt_raw ) < gc_data_row.
      RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = 'Template contains no data rows'.
    ENDIF.
  ENDMETHOD.

  METHOD read_binary.
    IF iv_server = abap_false.
      IF sy-batch = abap_true.
        RAISE EXCEPTION TYPE lcx_error
          EXPORTING iv_text = 'Local file cannot be read in background - use application server'.
      ENDIF.
      DATA: lt_bin TYPE solix_tab,
            lv_len TYPE i.
      cl_gui_frontend_services=>gui_upload(
        EXPORTING  filename   = iv_file
                   filetype   = 'BIN'
        IMPORTING  filelength = lv_len
        CHANGING   data_tab   = lt_bin
        EXCEPTIONS OTHERS     = 1 ).
      IF sy-subrc <> 0.
        RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = |Error uploading file { iv_file }|.
      ENDIF.
      rv_xdata = cl_bcs_convert=>solix_to_xstring( it_solix = lt_bin iv_size = lv_len ).
    ELSE.
      TRY.
          OPEN DATASET iv_file FOR INPUT IN BINARY MODE.
          IF sy-subrc <> 0.
            RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = |Cannot open file { iv_file }|.
          ENDIF.
          READ DATASET iv_file INTO rv_xdata.
          CLOSE DATASET iv_file.
        CATCH cx_sy_file_open cx_sy_file_authority cx_sy_file_io INTO DATA(lx_file).
          RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = lx_file->get_text( ).
      ENDTRY.
    ENDIF.
  ENDMETHOD.

  METHOD read_text_lines.
    DATA lv_line TYPE string.

    IF iv_server = abap_false.
      IF sy-batch = abap_true.
        RAISE EXCEPTION TYPE lcx_error
          EXPORTING iv_text = 'Local file cannot be read in background - use application server'.
      ENDIF.
      cl_gui_frontend_services=>gui_upload(
        EXPORTING  filename = iv_file
                   filetype = 'ASC'
        CHANGING   data_tab = rt_lines
        EXCEPTIONS OTHERS   = 1 ).
      IF sy-subrc <> 0.
        RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = |Error uploading file { iv_file }|.
      ENDIF.
    ELSE.
      TRY.
          OPEN DATASET iv_file FOR INPUT IN TEXT MODE ENCODING DEFAULT
                                   SKIPPING BYTE-ORDER MARK.
          IF sy-subrc <> 0.
            RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = |Cannot open file { iv_file }|.
          ENDIF.
          DO.
            READ DATASET iv_file INTO lv_line.
            IF sy-subrc <> 0.
              EXIT.
            ENDIF.
            APPEND lv_line TO rt_lines.
          ENDDO.
          CLOSE DATASET iv_file.
        CATCH cx_sy_file_open cx_sy_file_authority cx_sy_file_io
              cx_sy_conversion_codepage INTO DATA(lx_file).
          RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = lx_file->get_text( ).
      ENDTRY.
    ENDIF.

    "Remove UTF-8 BOM and CR
    IF rt_lines IS NOT INITIAL.
      ASSIGN rt_lines[ 1 ] TO FIELD-SYMBOL(<lv_first>).
      REPLACE ALL OCCURRENCES OF cl_abap_conv_in_ce=>uccp( 'FEFF' ) IN <lv_first> WITH ``.
    ENDIF.
    LOOP AT rt_lines ASSIGNING FIELD-SYMBOL(<lv_line>).
      REPLACE ALL OCCURRENCES OF cl_abap_char_utilities=>cr_lf(1) IN <lv_line> WITH ``.
    ENDLOOP.
  ENDMETHOD.

  METHOD parse_xlsx.
    FIELD-SYMBOLS: <lt_ws>   TYPE STANDARD TABLE,
                   <ls_line> TYPE any,
                   <lv_cell> TYPE any.
    DATA: lo_xl     TYPE REF TO cl_fdt_xl_spreadsheet,
          lt_values TYPE string_table.

    TRY.
        lo_xl = NEW #( document_name = iv_file xdocument = iv_xdata ).
      CATCH cx_fdt_excel_core INTO DATA(lx_xl).
        RAISE EXCEPTION TYPE lcx_error
          EXPORTING iv_text = |File is not a valid XLSX file: { lx_xl->get_text( ) }|.
    ENDTRY.

    lo_xl->if_fdt_doc_spreadsheet~get_worksheet_names( IMPORTING worksheet_names = DATA(lt_ws) ).
    IF lt_ws IS INITIAL.
      RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = 'XLSX file contains no worksheet'.
    ENDIF.

    "Template = first worksheet
    DATA(lr_data) = lo_xl->if_fdt_doc_spreadsheet~get_itab_from_worksheet( lt_ws[ 1 ] ).
    ASSIGN lr_data->* TO <lt_ws>.
    CHECK sy-subrc = 0.

    LOOP AT <lt_ws> ASSIGNING <ls_line>.
      CLEAR lt_values.
      DO.
        ASSIGN COMPONENT sy-index OF STRUCTURE <ls_line> TO <lv_cell>.
        IF sy-subrc <> 0.
          EXIT.
        ENDIF.
        APPEND CONV string( <lv_cell> ) TO lt_values.
      ENDDO.
      APPEND lt_values TO rt_raw.
    ENDLOOP.
  ENDMETHOD.

  METHOD parse_csv.
    CHECK it_lines IS NOT INITIAL.

    "Separator = most frequent of ; , TAB in the header line
    DATA(lv_hdr)   = it_lines[ 1 ].
    DATA(lv_tab)   = CONV string( cl_abap_char_utilities=>horizontal_tab ).
    DATA(lv_semi)  = count( val = lv_hdr sub = `;` ).
    DATA(lv_comma) = count( val = lv_hdr sub = `,` ).
    DATA(lv_tabs)  = count( val = lv_hdr sub = lv_tab ).
    DATA(lv_sep)   = COND string( WHEN lv_tabs > lv_semi AND lv_tabs > lv_comma THEN lv_tab
                                  WHEN lv_semi > lv_comma                     THEN `;`
                                  ELSE                                             `,` ).

    LOOP AT it_lines INTO DATA(lv_line).
      APPEND split_csv_line( iv_line = lv_line iv_sep = lv_sep ) TO rt_raw.
    ENDLOOP.
  ENDMETHOD.

  METHOD split_csv_line.
    "CSV with quoted fields ("a;b" and "" as escaped quote)
    DATA: lv_field  TYPE string,
          lv_quoted TYPE abap_bool,
          lv_pos    TYPE i.

    DATA(lv_len) = strlen( iv_line ).
    WHILE lv_pos < lv_len.
      DATA(lv_char) = substring( val = iv_line off = lv_pos len = 1 ).
      IF lv_quoted = abap_true.
        IF lv_char = `"`.
          DATA(lv_next) = lv_pos + 1.
          IF lv_next < lv_len AND substring( val = iv_line off = lv_next len = 1 ) = `"`.
            lv_field = lv_field && `"`.
            lv_pos = lv_pos + 1.
          ELSE.
            lv_quoted = abap_false.
          ENDIF.
        ELSE.
          lv_field = lv_field && lv_char.
        ENDIF.
      ELSEIF lv_char = `"`.
        lv_quoted = abap_true.
      ELSEIF lv_char = iv_sep.
        APPEND lv_field TO rt_fields.
        CLEAR lv_field.
      ELSE.
        lv_field = lv_field && lv_char.
      ENDIF.
      lv_pos = lv_pos + 1.
    ENDWHILE.
    APPEND lv_field TO rt_fields.
  ENDMETHOD.

ENDCLASS.

*======================================================================*
* LCL_CONFIG - variant, field catalogue, conditional mandatory rules
*======================================================================*
CLASS lcl_config IMPLEMENTATION.

  METHOD view_tables.
    "View table per selection-screen checkbox
    rt_tab = VALUE #( ( view = gc_view-basic  tabname = 'ZTMM_BASIC_DATA'  active = p_gen   )
                      ( view = gc_view-class  tabname = 'ZTMM_CLASS_DATA'  active = p_class )
                      ( view = gc_view-purch  tabname = 'ZTMM_PURCH_DATA'  active = p_purs  )
                      ( view = gc_view-mrp    tabname = 'ZTMM_MRP_DATA'    active = p_mrp   )
                      ( view = gc_view-plntst tabname = 'ZTMM_PLNTST_DATA' active = p_store )
                      ( view = gc_view-sales  tabname = 'ZTMM_SALES_DATA'  active = p_sales )
                      ( view = gc_view-val    tabname = 'ZTMM_VAL_DATA'    active = p_acct  ) ).
  ENDMETHOD.

  METHOD control_columns.
    "Template columns that steer processing (not in the view tables)
    rt_cols = VALUE #( ( gc_col-action )     ( gc_col-message )    ( gc_col-profile )
                       ( gc_col-ref_matnr )  ( gc_col-ref_werks )  ( gc_col-ref_vkorg )
                       ( gc_col-ref_vtweg )  ( gc_col-ref_ekorg )  ( gc_col-def_mode )
                       ( gc_col-copy_basic ) ( gc_col-copy_purch ) ( gc_col-copy_mrp )
                       ( gc_col-copy_sales ) ( gc_col-copy_acct ) ).
  ENDMETHOD.

  METHOD constructor.
    mo_log = io_log.
  ENDMETHOD.

  METHOD load.
    get_variant( ).        "5.2
    get_fields( ).         "5.3 / 5.4
    get_cond_rules( ).
  ENDMETHOD.

  METHOD get_variant.
    DATA(lv_opid) = lcl_screen=>get_operation( ).

    SELECT * FROM ztmm_matmas_mast
      INTO TABLE @DATA(lt_mast)
      WHERE mat_type     = @p_mtart
        AND ind_sec      = @p_indsec
        AND bus_prof     = @p_busprf
        AND operation_id = @lv_opid
        AND active_flag  = @abap_true
        AND valid_from  <= @sy-datum
        AND ( valid_to  >= @sy-datum OR valid_to = '00000000' ).

    IF lt_mast IS INITIAL.
      RAISE EXCEPTION TYPE lcx_error
        EXPORTING iv_text = |No active variant in ZTMM_MATMAS_MAST for { p_mtart } / { p_indsec } / | &&
                            |{ p_busprf } / operation { lv_opid }|.
    ENDIF.

    SORT lt_mast BY valid_from DESCENDING.
    mv_variant = lt_mast[ 1 ]-variant_view.

    IF lines( lt_mast ) > 1.
      mo_log->add( iv_type = 'W'
                   iv_text = |{ lines( lt_mast ) } active entries found - variant { mv_variant } | &&
                             |(latest valid-from) used| ).
    ENDIF.
    mo_log->add( iv_type = 'S' iv_text = |Active variant { mv_variant } determined| ).
  ENDMETHOD.

  METHOD get_fields.
    DATA lt_db TYPE STANDARD TABLE OF ztmm_basic_data WITH EMPTY KEY.

    CLEAR mt_fcat.
    DATA(lt_views) = view_tables( ).

    LOOP AT lt_views INTO DATA(ls_view) WHERE active = abap_true.
      CLEAR lt_db.
      TRY.
          "all view tables have the same structure -> dynamic table name
          SELECT * FROM (ls_view-tabname)
            INTO CORRESPONDING FIELDS OF TABLE @lt_db
            WHERE variant_view = @mv_variant.
        CATCH cx_sy_dynamic_osql_error INTO DATA(lx_sql).
          mo_log->add( iv_type = 'E' iv_text = |{ ls_view-tabname }: { lx_sql->get_text( ) }| ).
          CONTINUE.
      ENDTRY.

      IF lt_db IS INITIAL.
        mo_log->add( iv_type = 'W' iv_view = ls_view-view
                     iv_text = |No fields maintained in { ls_view-tabname } for variant { mv_variant }| ).
        CONTINUE.
      ENDIF.

      LOOP AT lt_db INTO DATA(ls_db).
        DATA(ls_fcat) = CORRESPONDING ty_fcat( ls_db ).
        ls_fcat-temp_field_name = to_upper( lcl_mapper=>trim( ls_fcat-temp_field_name ) ).
        ls_fcat-view            = ls_view-view.
        ls_fcat-targets         = parse_targets( ls_fcat ).
        APPEND ls_fcat TO mt_fcat.
      ENDLOOP.
    ENDLOOP.

    IF mt_fcat IS INITIAL.
      RAISE EXCEPTION TYPE lcx_error
        EXPORTING iv_text = |No field configuration found for variant { mv_variant } and the selected views|.
    ENDIF.
  ENDMETHOD.

  METHOD get_cond_rules.
    SELECT * FROM ztmm_cond_mand
      INTO TABLE @mt_cond
      WHERE mat_type     = @p_mtart
        AND ind_sec      = @p_indsec
        AND bus_prof     = @p_busprf
        AND variant_view = @mv_variant.

    LOOP AT mt_cond ASSIGNING FIELD-SYMBOL(<ls_cond>).
      <ls_cond>-source_field  = to_upper( lcl_mapper=>trim( <ls_cond>-source_field ) ).
      <ls_cond>-condmat_field = to_upper( lcl_mapper=>trim( <ls_cond>-condmat_field ) ).
    ENDLOOP.

    LOOP AT mt_fcat INTO DATA(ls_fcat) WHERE cond_mandatory = abap_true.
      IF NOT line_exists( mt_cond[ source_field = ls_fcat-temp_field_name ] ).
        mo_log->add( iv_type = 'W' iv_view = ls_fcat-view iv_field = ls_fcat-temp_field_name
                     iv_fdesc = ls_fcat-description
                     iv_text = 'Conditional mandatory, but no rule maintained in ZTMM_COND_MAND' ).
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD parse_targets.
    "BAPI_FIELD_NAME: target{,target}  target = [STRUCT-]FIELD{;QUAL=VALUE}
    DATA: lt_parts TYPE string_table,
          lt_quals TYPE string_table,
          lv_struct TYPE string,
          lv_comp   TYPE string.

    DATA(lv_def)     = to_upper( condense( val = CONV string( is_fcat-bapi_field_name )
                                           from = ` ` to = `` ) ).
    DATA(lv_def_str) = to_upper( lcl_mapper=>trim( is_fcat-bapi_struct_name ) ).

    IF lv_def IS INITIAL.
      IF is_fcat-system_derived = abap_false.
        mo_log->add( iv_type = 'W' iv_view = is_fcat-view iv_field = is_fcat-temp_field_name
                     iv_fdesc = is_fcat-description
                     iv_text = 'No BAPI field maintained - value is validated but not transferred' ).
      ENDIF.
      RETURN.
    ENDIF.

    SPLIT lv_def AT ',' INTO TABLE lt_parts.
    LOOP AT lt_parts INTO DATA(lv_part).
      SPLIT lv_part AT ';' INTO TABLE lt_quals.
      CHECK lt_quals IS NOT INITIAL.
      DATA(lv_tgt) = lt_quals[ 1 ].
      DELETE lt_quals INDEX 1.

      lv_struct = lv_def_str.
      lv_comp   = lv_tgt.
      IF lv_tgt CS '-'.
        SPLIT lv_tgt AT '-' INTO lv_struct lv_comp.
      ENDIF.

      DATA(ls_target) = VALUE ty_target( comp = lv_comp ).
      lcl_mapper=>resolve_param( EXPORTING iv_struct = lv_struct
                                 IMPORTING ev_param  = ls_target-param
                                           ev_table  = ls_target-table ).
      IF ls_target-param IS INITIAL.
        mo_log->add( iv_type = 'W' iv_view = is_fcat-view iv_field = is_fcat-temp_field_name
                     iv_fdesc = is_fcat-description
                     iv_text = |BAPI structure { lv_struct } not supported - target { lv_tgt } ignored| ).
        CONTINUE.
      ENDIF.

      LOOP AT lt_quals INTO DATA(lv_qual).
        SPLIT lv_qual AT '=' INTO DATA(lv_qkey) DATA(lv_qval).
        IF lv_qkey = 'LINE'.
          ls_target-linekey = lv_qval.
        ELSE.
          APPEND VALUE #( comp = lv_qkey value = lv_qval ) TO ls_target-fixed.
        ENDIF.
      ENDLOOP.

      IF lcl_mapper=>target_exists( ls_target ) = abap_false.
        mo_log->add( iv_type = 'W' iv_view = is_fcat-view iv_field = is_fcat-temp_field_name
                     iv_fdesc = is_fcat-description
                     iv_text = |Field { ls_target-param }-{ ls_target-comp } does not exist - target ignored| ).
        CONTINUE.
      ENDIF.
      APPEND ls_target TO rt_target.
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.

*======================================================================*
* LCL_MATERIAL_BAPI - simulate / post
*======================================================================*
CLASS lcl_material_bapi IMPLEMENTATION.

  METHOD constructor.
    mo_log = io_log.
  ENDMETHOD.

  METHOD get_material_number.
    FIELD-SYMBOLS <lv_num> TYPE any.
    DATA: lt_number TYPE STANDARD TABLE OF bapimatinr,
          ls_return TYPE bapireturn1.

    "External number from template
    IF lcl_mapper=>is_dummy_key( is_row-matkey ) = abap_false.
      CALL FUNCTION 'CONVERSION_EXIT_MATN1_INPUT'
        EXPORTING  input  = is_row-matkey
        IMPORTING  output = rv_matnr
        EXCEPTIONS OTHERS = 1.
      IF sy-subrc <> 0.
        CLEAR rv_matnr.
        mo_log->add( iv_type = 'E' is_row = is_row iv_text = 'Invalid material number' ).
      ENDIF.
      RETURN.
    ENDIF.

    "Internal numbering (Create only)
    IF lcl_screen=>get_operation( ) <> gc_op-create.
      mo_log->add( iv_type = 'E' is_row = is_row iv_text = 'MATNR is required for Update / Extend' ).
      RETURN.
    ENDIF.
    IF p_test = abap_true AND gc_sim_int_num = abap_false.
      mo_log->add( iv_type = 'W' is_row = is_row
                   iv_text = 'Simulation skipped - no MATNR (internal number is assigned at posting)' ).
      RETURN.
    ENDIF.

    CALL FUNCTION 'BAPI_MATERIAL_GETINTNUMBER'
      EXPORTING
        material_type    = p_mtart
        industry_sector  = p_indsec
        required_numbers = 1
      IMPORTING
        return           = ls_return
      TABLES
        material_number  = lt_number.
    IF ls_return-type CA 'EA' OR lt_number IS INITIAL.
      mo_log->add( iv_type = 'E' is_row = is_row
                   iv_text = |Internal material number not assigned: { ls_return-message }| ).
      RETURN.
    ENDIF.

    READ TABLE lt_number INTO DATA(ls_number) INDEX 1.
    ASSIGN COMPONENT 'MATERIAL_LONG' OF STRUCTURE ls_number TO <lv_num>.   "S/4HANA
    IF sy-subrc <> 0 OR <lv_num> IS INITIAL.
      ASSIGN COMPONENT 'MATERIAL' OF STRUCTURE ls_number TO <lv_num>.
    ENDIF.
    rv_matnr = <lv_num>.
    mo_log->add( iv_type = 'S' is_row = is_row iv_matnr = rv_matnr
                 iv_text = |Internal material number { rv_matnr ALPHA = OUT } assigned| ).
  ENDMETHOD.

  METHOD get_reference.
    "Read reference material via BAPI_MATERIAL_GET_ALL - called dynamically
    "so that the report also activates on releases without this BAPI
    FIELD-SYMBOLS <ls_ga> TYPE any.
    DATA: lt_ptab   TYPE abap_func_parmbind_tab,
          lt_return TYPE STANDARD TABLE OF bapiret2,
          lr_mara   TYPE REF TO data,
          lr_marc   TYPE REF TO data,
          lr_mpop   TYPE REF TO data,
          lr_mpgd   TYPE REF TO data,
          lr_mbew   TYPE REF TO data,
          lr_mvke   TYPE REF TO data,
          lv_mat18  TYPE c LENGTH 18,
          lv_mat40  TYPE c LENGTH 40,
          lv_bwkey  TYPE bwkey.

    DATA(lv_key) = |{ iv_matnr }/{ iv_werks }/{ iv_vkorg }/{ iv_vtweg }|.
    READ TABLE mt_cache INTO DATA(ls_cache) WITH KEY key = lv_key.
    IF sy-subrc = 0.
      rs_ref = ls_cache-data.
      RETURN.
    ENDIF.

    TRY.
        CREATE DATA lr_mara TYPE ('BAPI_MARA_GA').
        CREATE DATA lr_marc TYPE ('BAPI_MARC_GA').
        CREATE DATA lr_mpop TYPE ('BAPI_MPOP_GA').
        CREATE DATA lr_mpgd TYPE ('BAPI_MPGD_GA').
        CREATE DATA lr_mbew TYPE ('BAPI_MBEW_GA').
        CREATE DATA lr_mvke TYPE ('BAPI_MVKE_GA').
      CATCH cx_sy_create_data_error.
        RAISE EXCEPTION TYPE lcx_error
          EXPORTING iv_text = 'Reference copy not supported in this release (BAPI_MATERIAL_GET_ALL)'.
    ENDTRY.

    "S/4HANA: 40-char material number in MATERIAL_LONG
    cl_abap_typedescr=>describe_by_name( EXPORTING  p_name      = 'BAPIMATALL-MATERIAL_LONG'
                                         EXCEPTIONS type_not_found = 1
                                                    OTHERS         = 2 ).
    IF sy-subrc = 0.
      lv_mat40 = iv_matnr.
      INSERT VALUE #( name = 'MATERIAL_LONG' kind = abap_func_exporting value = REF #( lv_mat40 ) ) INTO TABLE lt_ptab.
    ELSE.
      lv_mat18 = iv_matnr.
      INSERT VALUE #( name = 'MATERIAL'      kind = abap_func_exporting value = REF #( lv_mat18 ) ) INTO TABLE lt_ptab.
    ENDIF.

    DATA(lv_werks) = iv_werks.
    DATA(lv_vkorg) = iv_vkorg.
    DATA(lv_vtweg) = iv_vtweg.
    lv_bwkey = iv_werks.
    IF lv_werks IS NOT INITIAL.
      INSERT VALUE #( name = 'PLANT'      kind = abap_func_exporting value = REF #( lv_werks ) ) INTO TABLE lt_ptab.
      INSERT VALUE #( name = 'VAL_AREA'   kind = abap_func_exporting value = REF #( lv_bwkey ) ) INTO TABLE lt_ptab.
    ENDIF.
    IF lv_vkorg IS NOT INITIAL.
      INSERT VALUE #( name = 'SALESORG'   kind = abap_func_exporting value = REF #( lv_vkorg ) ) INTO TABLE lt_ptab.
      INSERT VALUE #( name = 'DISTR_CHAN' kind = abap_func_exporting value = REF #( lv_vtweg ) ) INTO TABLE lt_ptab.
    ENDIF.
    INSERT VALUE #( name = 'CLIENTDATA'         kind = abap_func_importing value = lr_mara ) INTO TABLE lt_ptab.
    INSERT VALUE #( name = 'PLANTDATA'          kind = abap_func_importing value = lr_marc ) INTO TABLE lt_ptab.
    INSERT VALUE #( name = 'FORECASTPARAMETERS' kind = abap_func_importing value = lr_mpop ) INTO TABLE lt_ptab.
    INSERT VALUE #( name = 'PLANNINGDATA'       kind = abap_func_importing value = lr_mpgd ) INTO TABLE lt_ptab.
    INSERT VALUE #( name = 'VALUATIONDATA'      kind = abap_func_importing value = lr_mbew ) INTO TABLE lt_ptab.
    INSERT VALUE #( name = 'SALESDATA'          kind = abap_func_importing value = lr_mvke ) INTO TABLE lt_ptab.
    INSERT VALUE #( name = 'RETURN'             kind = abap_func_tables    value = REF #( lt_return ) ) INTO TABLE lt_ptab.

    TRY.
        CALL FUNCTION 'BAPI_MATERIAL_GET_ALL' PARAMETER-TABLE lt_ptab.
      CATCH cx_sy_dyn_call_error INTO DATA(lx_dyn).
        RAISE EXCEPTION TYPE lcx_error
          EXPORTING iv_text = |Reference material could not be read: { lx_dyn->get_text( ) }|.
    ENDTRY.

    LOOP AT lt_return INTO DATA(ls_ret) WHERE type CA 'EA'.
      RAISE EXCEPTION TYPE lcx_error
        EXPORTING iv_text = |Reference material { iv_matnr ALPHA = OUT }: { ls_ret-message }|.
    ENDLOOP.

    ASSIGN lr_mara->* TO <ls_ga>. MOVE-CORRESPONDING <ls_ga> TO rs_ref-clientdata.
    ASSIGN lr_marc->* TO <ls_ga>. MOVE-CORRESPONDING <ls_ga> TO rs_ref-plantdata.
    ASSIGN lr_mpop->* TO <ls_ga>. MOVE-CORRESPONDING <ls_ga> TO rs_ref-forecastparameters.
    ASSIGN lr_mpgd->* TO <ls_ga>. MOVE-CORRESPONDING <ls_ga> TO rs_ref-planningdata.
    ASSIGN lr_mbew->* TO <ls_ga>. MOVE-CORRESPONDING <ls_ga> TO rs_ref-valuationdata.
    ASSIGN lr_mvke->* TO <ls_ga>. MOVE-CORRESPONDING <ls_ga> TO rs_ref-salesdata.

    APPEND VALUE #( key = lv_key data = rs_ref ) TO mt_cache.
  ENDMETHOD.

  METHOD save_material.
    "BAPI_MATERIAL_SAVEREPLICA - one call per material with all org. levels
    "Test run: TESTRUN = 'X' -> complete check without database update
    FIELD-SYMBOLS: <lv_param> TYPE any,
                   <lv_line>  TYPE any.
    DATA: ls_call   TYPE ty_call,
          ls_return TYPE bapiretm,
          lt_retmsg TYPE STANDARD TABLE OF bapie1ret2.

    ls_call = is_call.                          "TABLES parameters must be changeable
    DATA(ls_first) = VALUE ty_row( it_rows[ 1 ] OPTIONAL ).

    CALL FUNCTION 'BAPI_MATERIAL_SAVEREPLICA'
      EXPORTING
        noappllog            = abap_true
        nochangedoc          = abap_false
        testrun              = p_test
        inpfldcheck          = space
      IMPORTING
        return               = ls_return
      TABLES
        headdata             = ls_call-headdata
        clientdata           = ls_call-clientdata
        clientdatax          = ls_call-clientdatax
        plantdata            = ls_call-plantdata
        plantdatax           = ls_call-plantdatax
        forecastparameters   = ls_call-forecastparameters
        forecastparametersx  = ls_call-forecastparametersx
        planningdata         = ls_call-planningdata
        planningdatax        = ls_call-planningdatax
        storagelocationdata  = ls_call-storagelocationdata
        storagelocationdatax = ls_call-storagelocationdatax
        unitsofmeasure       = ls_call-unitsofmeasure
        unitsofmeasurex      = ls_call-unitsofmeasurex
        internationalartnos  = ls_call-internationalartnos
        materiallongtext     = ls_call-materiallongtext
        taxclassifications   = ls_call-taxclassifications
        valuationdata        = ls_call-valuationdata
        valuationdatax       = ls_call-valuationdatax
        warehousenumberdata  = ls_call-warehousenumberdata
        warehousenumberdatax = ls_call-warehousenumberdatax
        salesdata            = ls_call-salesdata
        salesdatax           = ls_call-salesdatax
        storagetypedata      = ls_call-storagetypedata
        storagetypedatax     = ls_call-storagetypedatax
        materialdescription  = ls_call-materialdescription
        returnmessages       = lt_retmsg.

    rv_ok = COND #( WHEN ls_return-type CA 'EA' THEN abap_false ELSE abap_true ).

    LOOP AT lt_retmsg ASSIGNING FIELD-SYMBOL(<ls_rm>) WHERE type CA 'EAW'.
      "Template row of the BAPI line the message refers to (PARAMETER / ROW)
      DATA(ls_row) = ls_first.
      ASSIGN COMPONENT 'PARAMETER' OF STRUCTURE <ls_rm> TO <lv_param>.
      IF sy-subrc = 0.
        ASSIGN COMPONENT 'ROW' OF STRUCTURE <ls_rm> TO <lv_line>.
        IF sy-subrc = 0.
          READ TABLE is_call-origin INTO DATA(ls_origin)
               WITH KEY param = to_upper( <lv_param> ) idx = <lv_line>.
          IF sy-subrc = 0.
            ls_row = VALUE #( it_rows[ row = ls_origin-row ] DEFAULT ls_first ).
          ENDIF.
        ENDIF.
      ENDIF.

      mo_log->add( iv_type  = COND #( WHEN <ls_rm>-type = 'W' THEN 'W' ELSE 'E' )
                   iv_text  = |[{ <ls_rm>-id }/{ <ls_rm>-number }] { <ls_rm>-message }|
                   is_row   = ls_row
                   iv_matnr = iv_matnr ).
      IF <ls_rm>-type CA 'EA'.
        rv_ok = abap_false.
      ENDIF.
    ENDLOOP.

    rv_ok = finish_luw(
      iv_ok    = rv_ok
      iv_what  = |Material ({ lines( is_call-plantdata ) } plant(s), | &&
                 |{ lines( is_call-salesdata ) } sales area(s), | &&
                 |{ lines( is_call-valuationdata ) } valuation area(s))|
      iv_msg   = COND string( WHEN ls_return-message IS INITIAL THEN `processed`
                              ELSE ls_return-message )
      is_row   = ls_first
      iv_matnr = iv_matnr ).
  ENDMETHOD.

  METHOD classify.
    DATA: lv_objkey TYPE bapi1003_key-object,
          lt_char   TYPE STANDARD TABLE OF bapi1003_alloc_values_char,
          lt_num    TYPE STANDARD TABLE OF bapi1003_alloc_values_num,
          lt_curr   TYPE STANDARD TABLE OF bapi1003_alloc_values_curr,
          lt_return TYPE STANDARD TABLE OF bapiret2.

    lv_objkey = iv_matnr.
    DATA(lv_class) = is_class-classkey-classnum.
    DATA(lv_ctype) = COND klassenart( WHEN is_class-classkey-classtype IS INITIAL
                                      THEN gc_def_classtype ELSE is_class-classkey-classtype ).

    "Existing assignment (+ current values, BAPI_OBJCL_CHANGE replaces all values)
    CALL FUNCTION 'BAPI_OBJCL_GETDETAIL'
      EXPORTING
        objectkey       = lv_objkey
        objecttable     = gc_objtab_mara
        classnum        = lv_class
        classtype       = lv_ctype
      TABLES
        allocvaluesnum  = lt_num
        allocvalueschar = lt_char
        allocvaluescurr = lt_curr
        return          = lt_return.
    DATA(lv_exists) = COND abap_bool( WHEN line_exists( lt_return[ type = 'E' ] )
                                      THEN abap_false ELSE abap_true ).

    "Template values overwrite existing values of the same characteristic
    LOOP AT is_class-allocvalueschar INTO DATA(ls_char).
      DELETE lt_char WHERE charact = ls_char-charact.
    ENDLOOP.
    APPEND LINES OF is_class-allocvalueschar TO lt_char.
    LOOP AT is_class-allocvaluesnum INTO DATA(ls_num).
      DELETE lt_num WHERE charact = ls_num-charact.
    ENDLOOP.
    APPEND LINES OF is_class-allocvaluesnum TO lt_num.
    LOOP AT is_class-allocvaluescurr INTO DATA(ls_curr).
      DELETE lt_curr WHERE charact = ls_curr-charact.
    ENDLOOP.
    APPEND LINES OF is_class-allocvaluescurr TO lt_curr.

    CLEAR lt_return.
    IF lv_exists = abap_true.
      CALL FUNCTION 'BAPI_OBJCL_CHANGE'
        EXPORTING
          objectkey          = lv_objkey
          objecttable        = gc_objtab_mara
          classnum           = lv_class
          classtype          = lv_ctype
          status             = '1'
        TABLES
          allocvaluesnumnew  = lt_num
          allocvaluescharnew = lt_char
          allocvaluescurrnew = lt_curr
          return             = lt_return.
    ELSE.
      CALL FUNCTION 'BAPI_OBJCL_CREATE'
        EXPORTING
          objectkeynew    = lv_objkey
          objecttablenew  = gc_objtab_mara
          classnumnew     = lv_class
          classtypenew    = lv_ctype
          status          = '1'
        TABLES
          allocvaluesnum  = lt_num
          allocvalueschar = lt_char
          allocvaluescurr = lt_curr
          return          = lt_return.
    ENDIF.

    rv_ok = abap_true.
    LOOP AT lt_return INTO DATA(ls_ret) WHERE type CA 'EAW'.
      mo_log->add( iv_type = COND #( WHEN ls_ret-type = 'W' THEN 'W' ELSE 'E' )
                   iv_text = |[{ ls_ret-id }/{ ls_ret-number }] { ls_ret-message }|
                   is_row = is_row iv_matnr = iv_matnr iv_view = gc_view-class ).
      IF ls_ret-type CA 'EA'.
        rv_ok = abap_false.
      ENDIF.
    ENDLOOP.

    rv_ok = finish_luw( iv_ok = rv_ok
                        iv_what = |Classification { lv_ctype }/{ lv_class }|
                        iv_msg = COND string( WHEN lv_exists = abap_true THEN `assignment changed`
                                              ELSE `assignment created` )
                        is_row = is_row iv_matnr = iv_matnr ).
  ENDMETHOD.

  METHOD finish_luw.
    "Test run: material BAPI ran with TESTRUN = 'X', classification is
    "undone by rollback - otherwise commit / rollback
    DATA ls_commit TYPE bapiret2.
    rv_ok = iv_ok.

    IF p_test = abap_true.
      CALL FUNCTION 'BAPI_TRANSACTION_ROLLBACK'.
      CALL FUNCTION 'DEQUEUE_ALL'.
      mo_log->add( iv_type = COND #( WHEN rv_ok = abap_true THEN 'S' ELSE 'E' )
                   iv_text = |Simulation { COND string( WHEN rv_ok = abap_true THEN `OK` ELSE `failed` ) } | &&
                             |- { iv_what }: { iv_msg }|
                   is_row = is_row iv_matnr = iv_matnr ).
    ELSEIF rv_ok = abap_true.
      CALL FUNCTION 'BAPI_TRANSACTION_COMMIT'
        EXPORTING wait   = abap_true
        IMPORTING return = ls_commit.
      IF ls_commit-type CA 'EA'.
        rv_ok = abap_false.
        mo_log->add( iv_type = 'E' is_row = is_row iv_matnr = iv_matnr
                     iv_text = |Commit failed - { iv_what }: { ls_commit-message }| ).
      ELSE.
        mo_log->add( iv_type = 'S' is_row = is_row iv_matnr = iv_matnr
                     iv_text = |Posted - { iv_what }: { iv_msg }| ).
      ENDIF.
    ELSE.
      CALL FUNCTION 'BAPI_TRANSACTION_ROLLBACK'.
      mo_log->add( iv_type = 'E' is_row = is_row iv_matnr = iv_matnr
                   iv_text = |Posting failed - { iv_what }: { iv_msg }| ).
    ENDIF.
  ENDMETHOD.

ENDCLASS.
