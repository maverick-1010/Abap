*&---------------------------------------------------------------------*
*& Include          ZMM_MATERIAL_MAINTENANCE_C03
*&---------------------------------------------------------------------*
*& Class implementations - part 2
*&   lcl_output, lcl_template, lcl_screen, lcl_app
*& (part 1 in ZMM_MATERIAL_MAINTENANCE_C02)
*&---------------------------------------------------------------------*
*======================================================================*
* LCL_OUTPUT - ALV, file on application server, e-mail
*======================================================================*
CLASS lcl_output IMPLEMENTATION.

  METHOD constructor.
    mo_log = io_log.
  ENDMETHOD.

  METHOD publish.
    mt_out = mo_log->mt_msg.
    CHECK build_alv( ) = abap_true.

    DATA(lv_xlsx) = to_xlsx( ).
    save_to_server( lv_xlsx ).
    send_mail( lv_xlsx ).

    "messages of save / mail step
    mt_out = mo_log->mt_msg.
    IF sy-batch = abap_false.
      mo_alv->refresh( ).
      mo_alv->display( ).
    ENDIF.
  ENDMETHOD.

  METHOD build_alv.
    TRY.
        cl_salv_table=>factory( IMPORTING r_salv_table = mo_alv
                                CHANGING  t_table      = mt_out ).
        mo_alv->get_functions( )->set_all( abap_true ).
        mo_alv->get_display_settings( )->set_list_header( CONV lvc_title(
          |Material { SWITCH string( lcl_screen=>get_operation( )
                                    WHEN gc_op-create THEN `Create`
                                    WHEN gc_op-update THEN `Update`
                                    ELSE `Extend` ) } - | &&
          |{ COND string( WHEN p_test = abap_true THEN `Test run` ELSE `Update run` ) }| ) ).

        DATA(lo_cols) = mo_alv->get_columns( ).
        lo_cols->set_optimize( ).
        CAST cl_salv_column_table( lo_cols->get_column( 'ICON' ) )->set_icon( if_salv_c_bool_sap=>true ).
        lo_cols->get_column( 'ICON'  )->set_long_text( 'Status' ).
        lo_cols->get_column( 'MSGTY' )->set_long_text( 'Type' ).
        lo_cols->get_column( 'ROW'   )->set_long_text( 'Template Row' ).
        lo_cols->get_column( 'MATNR' )->set_long_text( 'Material' ).
        lo_cols->get_column( 'VIEW'  )->set_long_text( 'View' ).
        lo_cols->get_column( 'FIELD' )->set_long_text( 'Template Field' ).
        lo_cols->get_column( 'FDESC' )->set_long_text( 'Field Description' ).
        lo_cols->get_column( 'TEXT'  )->set_long_text( 'Message' ).
        rv_ok = abap_true.
      CATCH cx_salv_msg cx_salv_not_found.
        MESSAGE 'Error building the output ALV'(e10) TYPE 'I'.
    ENDTRY.
  ENDMETHOD.

  METHOD to_xlsx.
    TRY.
        rv_xdata = mo_alv->to_xml( xml_type = if_salv_bs_xml=>c_type_xlsx ).
      CATCH cx_root.
        CLEAR rv_xdata.
    ENDTRY.
  ENDMETHOD.

  METHOD file_name.
    rv_name = |MATMAINT_{ lcl_screen=>get_operation( ) }_{ sy-datum }_{ sy-uzeit }.xlsx|.
  ENDMETHOD.

  METHOD save_to_server.
    CHECK p_file3 IS NOT INITIAL AND iv_xdata IS NOT INITIAL.

    "P_FILE3 = directory (ending with / or \) or complete file name
    DATA(lv_file) = p_file3.
    DATA(lv_last) = substring( val = lv_file off = strlen( lv_file ) - 1 len = 1 ).
    IF lv_last = `/` OR lv_last = `\`.
      lv_file = lv_file && file_name( ).
    ELSEIF lcl_file_reader=>get_extension( lv_file ) <> 'xlsx'.
      lv_file = lv_file && `.xlsx`.
    ENDIF.

    TRY.
        OPEN DATASET lv_file FOR OUTPUT IN BINARY MODE.
        IF sy-subrc <> 0.
          mo_log->add( iv_type = 'W' iv_text = |Output file { lv_file } could not be opened| ).
          RETURN.
        ENDIF.
        TRANSFER iv_xdata TO lv_file.
        CLOSE DATASET lv_file.
        mo_log->add( iv_type = 'S' iv_text = |Output stored on application server: { lv_file }| ).
      CATCH cx_sy_file_open cx_sy_file_authority cx_sy_file_io INTO DATA(lx_file).
        mo_log->add( iv_type = 'W' iv_text = |Output file not written: { lx_file->get_text( ) }| ).
    ENDTRY.
  ENDMETHOD.

  METHOD send_mail.
    DATA lt_body TYPE soli_tab.
    CHECK p_email IS NOT INITIAL.

    TRY.
        DATA(lo_send) = cl_bcs=>create_persistent( ).

        lt_body = VALUE #(
          ( line = |Material maintenance - { COND string( WHEN p_test = abap_true THEN `test run` ELSE `update run` ) }| )
          ( line = |Material type { p_mtart } / industry sector { p_indsec } / business profile { p_busprf }| )
          ( line = |Errors: { mo_log->count( 'E' ) }   Warnings: { mo_log->count( 'W' ) }   | &&
                   |Success: { mo_log->count( 'S' ) }| )
          ( line = `The detailed log is attached.` ) ).

        DATA(lo_doc) = cl_document_bcs=>create_document(
          i_type    = 'RAW'
          i_text    = lt_body
          i_subject = CONV so_obj_des( |Material maintenance log { sy-datum DATE = USER } { sy-uzeit TIME = USER }| ) ).

        IF iv_xdata IS NOT INITIAL.
          DATA(lv_name) = file_name( ).
          lo_doc->add_attachment(
            i_attachment_type    = 'BIN'
            i_attachment_subject = CONV so_obj_des( lv_name )
            i_attachment_size    = CONV so_obj_len( xstrlen( iv_xdata ) )
            i_att_content_hex    = cl_bcs_convert=>xstring_to_solix( iv_xdata )
            i_attachment_header  = VALUE soli_tab( ( line = |&SO_FILENAME={ lv_name }| ) ) ).
        ENDIF.

        lo_send->set_document( lo_doc ).
        lo_send->add_recipient( cl_cam_address_bcs=>create_internet_address( p_email ) ).
        lo_send->set_send_immediately( abap_true ).
        lo_send->send( ).
        COMMIT WORK.
        mo_log->add( iv_type = 'S' iv_text = |Output log sent to { p_email }| ).
      CATCH cx_bcs INTO DATA(lx_bcs).
        mo_log->add( iv_type = 'W' iv_text = |E-mail not sent: { lx_bcs->get_text( ) }| ).
    ENDTRY.
  ENDMETHOD.

ENDCLASS.

*======================================================================*
* LCL_TEMPLATE - upload template as .xlsx
*======================================================================*
CLASS lcl_template IMPLEMENTATION.

  METHOD template_columns.
    "Structure of the upload template (column order)
    DATA(lv_cols) =
      `ACTION MESSAGE PROCESS_PROFILE REFERENCE_MATNR REF_WERKS REF_VKORG REF_VTWEG REF_EKORG ` &&
      `DEFAULT_MODE COPY_BASIC COPY_PURCH COPY_MRP COPY_SALES COPY_ACCOUNTING ` &&
      `MATNR MTART MBRSH LGORT SPRAS MAKTX MEINS MATKL PRDHA EXTWG BRGEW NTGEW GEWEI VOLUM VOLEH ` &&
      `EAN11 NUMTP XCHPF IPRKZ MHDRZ MHDLP SERNP MTPOS_MARA SPART KZUMV LABOR LAENG BREIT HOEHE MEABM ` &&
      `CLASS_TYPE CLASS_NAME CHAR_NAME_1 CHAR_VALUE_1 CHAR_NAME_2 CHAR_VALUE_2 CHAR_NAME_3 CHAR_VALUE_3 ` &&
      `CHAR_NAME_4 CHAR_VALUE_4 CHAR_NAME_5 CHAR_VALUE_5 ` &&
      `VKORG VTWEG VMSTD MSTDV MTPOS KTGRM MVGR2 MVGR3 KONDM BONBA VRKME UMREZ UMREN VKGRU PROVG ` &&
      `TRAGR LADGR MTVFP AUTLF ANTLF AUMNG STAWN EXPME HERKL LOGGR CASNR MSTAV VALID_TO DWERK VERSG ` &&
      `MWST ZGST PRCTR ` &&
      `EKORG EKGRP PLIFZ BSTMI_P BSTMA_P BSTME_P INSMK KZKRI EINKZ UMLMC TAXIM AUTRU MFRPN MFRNR ` &&
      `WERKS DISMM DISPO DISLS BSTMA BSTFE MINBE EISBE MABST MTVFP_M FXHOR PERKZ BESKZ LGPRO LGFSB ` &&
      `FHORI DZEIT IPRKZ_M PRGRP PERIV SBDKZ KAUSF RGEKZ XCHAR2 RAUBE TEMPB MHDRZ2 MHDLP2 MAXLP ` &&
      `DISGR ABCIN BSTRF SHFLG SHZET STRGR VRMOD VINT1 VINT2 MTVFP2 CCFIX PRMOD ` &&
      `LGNUM LGTYP LGBKZ LTKZE LHMG1 LVSME LETY1 LTKZA ` &&
      `BWKEY BKLAS VPRSV STPRS VERPR BWTTY MLAST HKMAT ZKPRS ZKDAT ` &&
      `PO_TEXT PRODH_LVL1 PRODH_LVL2 PRODH_LVL3 PRODH_LVL4 PRODH_LVL5`.
    SPLIT lv_cols AT space INTO TABLE rt_cols.
    DELETE rt_cols WHERE table_line IS INITIAL.
  ENDMETHOD.

  METHOD download.
    DATA: lt_fcat    TYPE tt_fcat,
          lt_cols    TYPE tt_col,
          lv_variant TYPE string,
          lv_file    TYPE string,
          lv_path    TYPE string,
          lv_full    TYPE string,
          lv_action  TYPE i.

    "Field flags of the active variant (only if type / sector / profile selected)
    IF p_mtart IS NOT INITIAL AND p_indsec IS NOT INITIAL AND p_busprf IS NOT INITIAL.
      DATA(lo_cfg) = NEW lcl_config( NEW lcl_log( ) ).
      TRY.
          lo_cfg->load( ).
          lt_fcat    = lo_cfg->mt_fcat.
          lv_variant = lo_cfg->mv_variant.
        CATCH lcx_error.
          CLEAR: lt_fcat, lv_variant.
      ENDTRY.
    ENDIF.

    "Columns = template structure + fields of the variant not yet contained
    DATA(lt_names) = template_columns( ).
    LOOP AT lt_fcat INTO DATA(ls_fcat).
      IF NOT line_exists( lt_names[ table_line = ls_fcat-temp_field_name ] ).
        APPEND ls_fcat-temp_field_name TO lt_names.
      ENDIF.
    ENDLOOP.

    "Header colour per column
    DATA(lt_ctrl) = lcl_config=>control_columns( ).
    LOOP AT lt_names INTO DATA(lv_name).
      APPEND VALUE #(
        field = lv_name
        style = COND #(
          WHEN line_exists( lt_ctrl[ table_line = lv_name ] )
            THEN c_style-control
          WHEN line_exists( lt_fcat[ temp_field_name = lv_name mandatory = abap_true ] )
            THEN c_style-mandatory
          WHEN line_exists( lt_fcat[ temp_field_name = lv_name cond_mandatory = abap_true ] )
            THEN c_style-cond
          WHEN line_exists( lt_fcat[ temp_field_name = lv_name system_derived = abap_true ] ) AND
               NOT line_exists( lt_fcat[ temp_field_name = lv_name optional = abap_true ] )
            THEN c_style-system
          ELSE c_style-header ) ) TO lt_cols.
    ENDLOOP.

    DATA(lv_xlsx) = build_xlsx( it_cols = lt_cols it_fcat = lt_fcat iv_variant = lv_variant ).

    cl_gui_frontend_services=>file_save_dialog(
      EXPORTING  default_file_name = |Material_Template{ COND string( WHEN lv_variant IS NOT INITIAL
                                                                     THEN |_{ lv_variant }| ) }.xlsx|
                 default_extension = 'xlsx'
                 file_filter       = 'Excel (*.xlsx)|*.xlsx'
      CHANGING   filename          = lv_file
                 path              = lv_path
                 fullpath          = lv_full
                 user_action       = lv_action
      EXCEPTIONS OTHERS            = 1 ).
    CHECK sy-subrc = 0 AND lv_action = cl_gui_frontend_services=>action_ok.

    DATA(lt_bin) = cl_bcs_convert=>xstring_to_solix( lv_xlsx ).
    cl_gui_frontend_services=>gui_download(
      EXPORTING  bin_filesize = xstrlen( lv_xlsx )
                 filename     = lv_full
                 filetype     = 'BIN'
      CHANGING   data_tab     = lt_bin
      EXCEPTIONS OTHERS       = 1 ).
    IF sy-subrc = 0.
      MESSAGE |Template downloaded to { lv_full }| TYPE 'S'.
    ELSE.
      MESSAGE 'Template could not be downloaded'(e11) TYPE 'S' DISPLAY LIKE 'E'.
    ENDIF.
  ENDMETHOD.

  METHOD build_xlsx.
    DATA(lo_zip) = NEW cl_abap_zip( ).

    lo_zip->add( name    = '[Content_Types].xml'
                 content = utf8(
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` &&
      `<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">` &&
      `<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>` &&
      `<Default Extension="xml" ContentType="application/xml"/>` &&
      `<Override PartName="/xl/workbook.xml" ` &&
      `ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>` &&
      `<Override PartName="/xl/worksheets/sheet1.xml" ` &&
      `ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>` &&
      `<Override PartName="/xl/worksheets/sheet2.xml" ` &&
      `ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>` &&
      `<Override PartName="/xl/styles.xml" ` &&
      `ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>` &&
      `</Types>` ) ).

    lo_zip->add( name    = '_rels/.rels'
                 content = utf8(
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` &&
      `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">` &&
      `<Relationship Id="rId1" ` &&
      `Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" ` &&
      `Target="xl/workbook.xml"/>` &&
      `</Relationships>` ) ).

    lo_zip->add( name    = 'xl/workbook.xml'
                 content = utf8(
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` &&
      `<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" ` &&
      `xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">` &&
      `<sheets><sheet name="TEMPLATE" sheetId="1" r:id="rId1"/>` &&
      `<sheet name="FIELD_INFO" sheetId="2" r:id="rId2"/></sheets>` &&
      `</workbook>` ) ).

    lo_zip->add( name    = 'xl/_rels/workbook.xml.rels'
                 content = utf8(
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` &&
      `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">` &&
      `<Relationship Id="rId1" ` &&
      `Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" ` &&
      `Target="worksheets/sheet1.xml"/>` &&
      `<Relationship Id="rId2" ` &&
      `Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" ` &&
      `Target="worksheets/sheet2.xml"/>` &&
      `<Relationship Id="rId3" ` &&
      `Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" ` &&
      `Target="styles.xml"/>` &&
      `</Relationships>` ) ).

    lo_zip->add( name = 'xl/styles.xml'            content = utf8( styles( ) ) ).
    lo_zip->add( name = 'xl/worksheets/sheet1.xml' content = utf8( sheet_template( it_cols ) ) ).
    lo_zip->add( name = 'xl/worksheets/sheet2.xml' content = utf8( sheet_info( it_fcat    = it_fcat
                                                                               iv_variant = iv_variant ) ) ).
    rv_xlsx = lo_zip->save( ).
  ENDMETHOD.

  METHOD sheet_template.
    "Sheet 1 = upload template: row 1 technical field names, data from row 2
    DATA lv_cells TYPE string.

    LOOP AT it_cols INTO DATA(ls_col).
      DATA(lv_idx) = sy-tabix.
      lv_cells = lv_cells && cell( iv_col = lv_idx iv_row = 1 iv_value = ls_col-field iv_style = ls_col-style ).
    ENDLOOP.

    rv_xml =
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` &&
      `<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">` &&
      `<sheetViews><sheetView workbookViewId="0">` &&
      `<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>` &&
      `</sheetView></sheetViews>` &&
      |<cols><col min="1" max="{ lines( it_cols ) }" width="18" style="{ c_style-text }" customWidth="1"/></cols>| &&
      |<sheetData><row r="1">{ lv_cells }</row></sheetData>| &&
      `</worksheet>`.
  ENDMETHOD.

  METHOD sheet_info.
    "Sheet 2 = instructions, colour legend and field list of the variant
    TYPES: BEGIN OF lty_line,
             style  TYPE i,
             values TYPE string_table,
           END OF lty_line.
    DATA: lt_lines TYPE STANDARD TABLE OF lty_line WITH EMPTY KEY,
          lv_rows  TYPE string,
          lv_cells TYPE string.

    APPEND VALUE #( style  = c_style-bold
                    values = VALUE #( ( COND string( WHEN iv_variant IS INITIAL
                                                     THEN `Material upload template`
                                                     ELSE |Material upload template - variant { iv_variant }| ) ) ) )
      TO lt_lines.
    APPEND VALUE #( values = VALUE #(
      ( `Fill sheet TEMPLATE from row 2. Do not change row 1 (technical field names) - only the first worksheet is read.` ) ) )
      TO lt_lines.
    APPEND VALUE #( values = VALUE #(
      ( `One row per material and org. level (plant / sales area / valuation area). Save as .xlsx or .csv.` ) ) )
      TO lt_lines.
    APPEND INITIAL LINE TO lt_lines.
    APPEND VALUE #( style = c_style-bold      values = VALUE #( ( `Header colour` ) ( `Meaning` ) ) ) TO lt_lines.
    APPEND VALUE #( style = c_style-control   values = VALUE #( ( `Green` )  ( `Control column (action, reference copy)` ) ) ) TO lt_lines.
    APPEND VALUE #( style = c_style-mandatory values = VALUE #( ( `Red` )    ( `Mandatory for the variant` ) ) ) TO lt_lines.
    APPEND VALUE #( style = c_style-cond      values = VALUE #( ( `Orange` ) ( `Conditional mandatory (rules in ZTMM_COND_MAND)` ) ) ) TO lt_lines.
    APPEND VALUE #( style = c_style-system    values = VALUE #( ( `Grey` )   ( `System derived - value is not used` ) ) ) TO lt_lines.
    APPEND VALUE #( style = c_style-header    values = VALUE #( ( `Blue` )   ( `Optional / not maintained for the variant` ) ) ) TO lt_lines.
    APPEND INITIAL LINE TO lt_lines.

    IF it_fcat IS INITIAL.
      APPEND VALUE #( values = VALUE #(
        ( `Select material type, industry sector and business profile before downloading ` &&
          `to get the field flags of the active variant.` ) ) ) TO lt_lines.
    ELSE.
      APPEND VALUE #( style  = c_style-bold
                      values = VALUE #( ( `Field` ) ( `Description` ) ( `View` ) ( `Flag` ) ( `BAPI target` ) ) )
        TO lt_lines.
      LOOP AT it_fcat INTO DATA(ls_fcat).
        APPEND VALUE #(
          style  = c_style-text
          values = VALUE #(
            ( CONV string( ls_fcat-temp_field_name ) )
            ( CONV string( ls_fcat-description ) )
            ( CONV string( ls_fcat-view ) )
            ( COND string( WHEN ls_fcat-mandatory      = abap_true THEN `Mandatory`
                           WHEN ls_fcat-cond_mandatory = abap_true THEN `Conditional mandatory`
                           WHEN ls_fcat-optional       = abap_true THEN `Optional`
                           WHEN ls_fcat-system_derived = abap_true THEN `System derived`
                           ELSE `Optional` ) )
            ( condense( |{ ls_fcat-bapi_struct_name } { ls_fcat-bapi_field_name }| ) ) ) )
          TO lt_lines.
      ENDLOOP.
    ENDIF.

    LOOP AT lt_lines INTO DATA(ls_line).
      DATA(lv_row) = sy-tabix.
      CLEAR lv_cells.
      LOOP AT ls_line-values INTO DATA(lv_value).
        DATA(lv_col) = sy-tabix.
        lv_cells = lv_cells && cell( iv_col = lv_col iv_row = lv_row iv_value = lv_value iv_style = ls_line-style ).
      ENDLOOP.
      lv_rows = lv_rows && |<row r="{ lv_row }">{ lv_cells }</row>|.
    ENDLOOP.

    rv_xml =
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` &&
      `<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">` &&
      `<cols><col min="1" max="1" width="22" customWidth="1"/>` &&
      `<col min="2" max="2" width="55" customWidth="1"/>` &&
      `<col min="3" max="5" width="24" customWidth="1"/></cols>` &&
      |<sheetData>{ lv_rows }</sheetData>| &&
      `</worksheet>`.
  ENDMETHOD.

  METHOD styles.
    "Fonts: 0 Arial, 1 Arial bold white, 2 Arial bold
    "Fills: 2 blue, 3 red, 4 orange, 5 grey, 6 green
    "cellXfs: see C_STYLE
    rv_xml =
      `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` &&
      `<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">` &&
      `<fonts count="3">` &&
      `<font><sz val="10"/><name val="Arial"/></font>` &&
      `<font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Arial"/></font>` &&
      `<font><b/><sz val="10"/><name val="Arial"/></font>` &&
      `</fonts>` &&
      `<fills count="7">` &&
      `<fill><patternFill patternType="none"/></fill>` &&
      `<fill><patternFill patternType="gray125"/></fill>` &&
      `<fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill>` &&
      `<fill><patternFill patternType="solid"><fgColor rgb="FFC00000"/><bgColor indexed="64"/></patternFill></fill>` &&
      `<fill><patternFill patternType="solid"><fgColor rgb="FFED7D31"/><bgColor indexed="64"/></patternFill></fill>` &&
      `<fill><patternFill patternType="solid"><fgColor rgb="FF7F7F7F"/><bgColor indexed="64"/></patternFill></fill>` &&
      `<fill><patternFill patternType="solid"><fgColor rgb="FF548235"/><bgColor indexed="64"/></patternFill></fill>` &&
      `</fills>` &&
      `<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>` &&
      `<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>` &&
      `<cellXfs count="8">` &&
      `<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>` &&
      `<xf numFmtId="49" fontId="1" fillId="2" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1"/>` &&
      `<xf numFmtId="49" fontId="1" fillId="3" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1"/>` &&
      `<xf numFmtId="49" fontId="1" fillId="4" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1"/>` &&
      `<xf numFmtId="49" fontId="1" fillId="5" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1"/>` &&
      `<xf numFmtId="49" fontId="1" fillId="6" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1"/>` &&
      `<xf numFmtId="49" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>` &&
      `<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>` &&
      `</cellXfs>` &&
      `<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>` &&
      `</styleSheet>`.
  ENDMETHOD.

  METHOD cell.
    rv_xml = |<c r="{ col_letter( iv_col ) }{ iv_row }" t="inlineStr" s="{ iv_style }">| &&
             |<is><t xml:space="preserve">| &&
             escape( val = CONV string( iv_value ) format = cl_abap_format=>e_xml_text ) &&
             |</t></is></c>|.
  ENDMETHOD.

  METHOD col_letter.
    "1 -> A, 26 -> Z, 27 -> AA ...
    DATA(lv_n) = iv_col.
    WHILE lv_n > 0.
      DATA(lv_m) = ( lv_n - 1 ) MOD 26.
      rv_col = substring( val = sy-abcde off = lv_m len = 1 ) && rv_col.
      lv_n = ( lv_n - 1 ) DIV 26.
    ENDWHILE.
  ENDMETHOD.

  METHOD utf8.
    rv_x = cl_abap_codepage=>convert_to( iv_xml ).
  ENDMETHOD.

ENDCLASS.

*======================================================================*
* LCL_SCREEN - selection screen
*======================================================================*
CLASS lcl_screen IMPLEMENTATION.

  METHOD initialization.
    p_btn = 'Download Template'(b01).
  ENDMETHOD.

  METHOD get_operation.
    rv_opid = COND #( WHEN r_create = abap_true THEN gc_op-create
                      WHEN r_update = abap_true THEN gc_op-update
                      ELSE                           gc_op-extend ).
  ENDMETHOD.

  METHOD pbo.
    LOOP AT SCREEN.
      CASE screen-group1.
        WHEN 'MD1'.
          screen-input = COND #( WHEN r_local = abap_true THEN '1' ELSE '0' ).
        WHEN 'MD2'.
          screen-input = COND #( WHEN r_unix  = abap_true THEN '1' ELSE '0' ).
      ENDCASE.
      MODIFY SCREEN.
    ENDLOOP.
    set_listboxes( ).
  ENDMETHOD.

  METHOD set_listboxes.
    "Only values allowed in ZTMM_MATMAS_MAST for the selected action
    DATA: lt_vrm    TYPE vrm_values,
          lt_mtart  TYPE STANDARD TABLE OF mtart         WITH EMPTY KEY,
          lt_indsec TYPE STANDARD TABLE OF z_de_ind_sec  WITH EMPTY KEY,
          lt_busprf TYPE STANDARD TABLE OF z_de_bus_prof WITH EMPTY KEY,
          lr_mtart  TYPE RANGE OF mtart,
          lr_indsec TYPE RANGE OF z_de_ind_sec.

    DATA(lv_opid) = get_operation( ).

    "--- Material type
    SELECT DISTINCT mat_type FROM ztmm_matmas_mast
      INTO TABLE @lt_mtart
      WHERE operation_id = @lv_opid
        AND active_flag  = @abap_true
        AND valid_from  <= @sy-datum
        AND ( valid_to  >= @sy-datum OR valid_to = '00000000' ).
    IF lt_mtart IS NOT INITIAL.
      SELECT mtart, mtbez FROM t134t
        INTO TABLE @DATA(lt_t134t)
        FOR ALL ENTRIES IN @lt_mtart
        WHERE spras = @sy-langu AND mtart = @lt_mtart-table_line.
    ENDIF.
    lt_vrm = VALUE #( FOR lv_mtart IN lt_mtart
                      ( key  = lv_mtart
                        text = VALUE #( lt_t134t[ mtart = lv_mtart ]-mtbez OPTIONAL ) ) ).
    CALL FUNCTION 'VRM_SET_VALUES' EXPORTING id = 'P_MTART' values = lt_vrm EXCEPTIONS OTHERS = 0.
    IF p_mtart IS NOT INITIAL AND NOT line_exists( lt_mtart[ table_line = p_mtart ] ).
      CLEAR p_mtart.
    ENDIF.

    "--- Industry sector (for material type)
    IF p_mtart IS NOT INITIAL.
      lr_mtart = VALUE #( ( sign = 'I' option = 'EQ' low = p_mtart ) ).
    ENDIF.
    SELECT DISTINCT ind_sec FROM ztmm_matmas_mast
      INTO TABLE @lt_indsec
      WHERE operation_id = @lv_opid
        AND active_flag  = @abap_true
        AND mat_type    IN @lr_mtart
        AND valid_from  <= @sy-datum
        AND ( valid_to  >= @sy-datum OR valid_to = '00000000' ).
    IF lt_indsec IS NOT INITIAL.
      SELECT mbrsh, mbbez FROM t137t
        INTO TABLE @DATA(lt_t137t)
        FOR ALL ENTRIES IN @lt_indsec
        WHERE spras = @sy-langu AND mbrsh = @lt_indsec-table_line.
    ENDIF.
    lt_vrm = VALUE #( FOR lv_ind IN lt_indsec
                      ( key  = lv_ind
                        text = VALUE #( lt_t137t[ mbrsh = lv_ind ]-mbbez OPTIONAL ) ) ).
    CALL FUNCTION 'VRM_SET_VALUES' EXPORTING id = 'P_INDSEC' values = lt_vrm EXCEPTIONS OTHERS = 0.
    IF p_indsec IS NOT INITIAL AND NOT line_exists( lt_indsec[ table_line = p_indsec ] ).
      CLEAR p_indsec.
    ENDIF.

    "--- Business profile (for material type + industry sector)
    IF p_indsec IS NOT INITIAL.
      lr_indsec = VALUE #( ( sign = 'I' option = 'EQ' low = p_indsec ) ).
    ENDIF.
    SELECT DISTINCT bus_prof FROM ztmm_matmas_mast
      INTO TABLE @lt_busprf
      WHERE operation_id = @lv_opid
        AND active_flag  = @abap_true
        AND mat_type    IN @lr_mtart
        AND ind_sec     IN @lr_indsec
        AND valid_from  <= @sy-datum
        AND ( valid_to  >= @sy-datum OR valid_to = '00000000' ).
    lt_vrm = VALUE #( FOR lv_bp IN lt_busprf ( key = lv_bp text = lv_bp ) ).
    CALL FUNCTION 'VRM_SET_VALUES' EXPORTING id = 'P_BUSPRF' values = lt_vrm EXCEPTIONS OTHERS = 0.
    IF p_busprf IS NOT INITIAL AND NOT line_exists( lt_busprf[ table_line = p_busprf ] ).
      CLEAR p_busprf.
    ENDIF.
  ENDMETHOD.

  METHOD pai.
    CASE sscrfields-ucomm.
      WHEN 'BTN_CLK'.
        download_template( ).
      WHEN 'ONLI' OR 'SJOB' OR 'PRIN'.
        check_input( ).
    ENDCASE.
  ENDMETHOD.

  METHOD check_input.
    IF p_mtart IS INITIAL OR p_indsec IS INITIAL OR p_busprf IS INITIAL.
      MESSAGE 'Select material type, industry sector and business profile'(e01) TYPE 'E'.
    ENDIF.
    IF p_gen IS INITIAL AND p_sales IS INITIAL AND p_purs  IS INITIAL AND
       p_mrp IS INITIAL AND p_store IS INITIAL AND p_acct IS INITIAL AND p_class IS INITIAL.
      MESSAGE 'Select at least one view'(e02) TYPE 'E'.
    ENDIF.
    DATA(lv_file) = COND string( WHEN r_local = abap_true THEN p_file1 ELSE p_file2 ).
    IF lv_file IS INITIAL.
      MESSAGE 'Enter the template file path'(e03) TYPE 'E'.
    ENDIF.
    DATA(lv_ext) = lcl_file_reader=>get_extension( lv_file ).
    IF lv_ext <> 'xlsx' AND lv_ext <> 'csv'.
      MESSAGE 'Only .xlsx and .csv files are allowed'(e04) TYPE 'E'.
    ENDIF.
  ENDMETHOD.

  METHOD f4_local_file.
    DATA: lt_files TYPE filetable,
          lv_rc    TYPE i.
    cl_gui_frontend_services=>file_open_dialog(
      EXPORTING  file_filter = 'Excel (*.xlsx)|*.xlsx|CSV (*.csv)|*.csv'
      CHANGING   file_table  = lt_files
                 rc          = lv_rc
      EXCEPTIONS OTHERS      = 1 ).
    IF sy-subrc = 0 AND lv_rc > 0.
      cv_file = lt_files[ 1 ]-filename.
    ENDIF.
  ENDMETHOD.

  METHOD download_template.
    "Upload template (.xlsx) as reference for the user
    lcl_template=>download( ).
  ENDMETHOD.

ENDCLASS.

*======================================================================*
* LCL_APP - controller
*======================================================================*
CLASS lcl_app IMPLEMENTATION.

  METHOD constructor.
    mo_log    = NEW #( ).
    mo_config = NEW #( mo_log ).
    mo_bapi   = NEW #( mo_log ).
  ENDMETHOD.

  METHOD run.
    TRY.
        mo_config->load( ).          "5.2 variant, 5.3/5.4 view tables
        load_template( ).            "5.1 read template
        derive_values( ).
        check_columns( ).
        validate_and_map( ).         "5.5 validation + mapping to BAPI
      CATCH lcx_error INTO DATA(lx_error).
        mo_log->add( iv_type = 'E' iv_text = lx_error->get_text( ) ).
    ENDTRY.

    DATA(lv_err) = mo_log->count( 'E' ).
    mo_log->add( iv_type = COND #( WHEN lv_err > 0 THEN 'W' ELSE 'S' )
                 iv_text = |Validation finished: { lines( mt_row ) } row(s), { lv_err } error(s), | &&
                           |{ mo_log->count( 'W' ) } warning(s)| ).

    IF mo_log->has_global_error( ) = abap_true.
      mo_log->add( iv_type = 'E'
                   iv_text = |{ COND string( WHEN p_test = abap_true THEN `Simulation` ELSE `Posting` ) } | &&
                             |not executed - correct the errors first| ).
    ELSE.
      process_materials( ).        "simulate / post
    ENDIF.

    NEW lcl_output( mo_log )->publish( ).
  ENDMETHOD.

*----------------------------------------------------------------------*
* 5.1 - template
*----------------------------------------------------------------------*
  METHOD load_template.
    DATA lv_has_data TYPE abap_bool.

    DATA(lv_file) = COND string( WHEN r_local = abap_true THEN p_file1 ELSE p_file2 ).
    DATA(lt_raw)  = lcl_file_reader=>read( iv_file = lv_file iv_server = r_unix ).

    "Header row: column index -> technical field name
    DATA(lt_hdr) = lt_raw[ gc_hdr_row ].
    LOOP AT lt_hdr INTO DATA(lv_hdr).
      DATA(lv_field) = CONV fieldname( to_upper( lcl_mapper=>trim( lv_hdr ) ) ).
      IF lv_field IS NOT INITIAL AND line_exists( mt_header[ table_line = lv_field ] ).
        mo_log->add( iv_type = 'W' iv_field = lv_field iv_text = 'Duplicate column - first occurrence used' ).
        CLEAR lv_field.
      ENDIF.
      APPEND lv_field TO mt_header.
    ENDLOOP.

    "Data rows: keep non-empty cells only
    LOOP AT lt_raw INTO DATA(lt_values) FROM gc_data_row.
      DATA(lv_row) = sy-tabix.                            "= row number in the file
      lv_has_data = abap_false.

      LOOP AT lt_values INTO DATA(lv_raw).
        DATA(lv_col) = sy-tabix.
        DATA(lv_colname) = VALUE fieldname( mt_header[ lv_col ] OPTIONAL ).
        CHECK lv_colname IS NOT INITIAL AND lv_colname <> gc_col-message.
        DATA(lv_value) = lcl_mapper=>trim( lv_raw ).
        CHECK lv_value IS NOT INITIAL.
        INSERT VALUE #( row = lv_row field = lv_colname value = lv_value ) INTO TABLE mt_cell.
        lv_has_data = abap_true.
      ENDLOOP.

      CHECK lv_has_data = abap_true.                      "skip empty lines
      DATA(lv_matnr) = to_upper( get_value( iv_row = lv_row iv_field = gc_col-matnr ) ).
      APPEND VALUE #( row    = lv_row
                      matkey = COND #( WHEN lv_matnr IS INITIAL THEN |#{ lv_row }| ELSE lv_matnr )
                      werks  = to_upper( get_value( iv_row = lv_row iv_field = gc_col-werks ) )
                      vkorg  = to_upper( get_value( iv_row = lv_row iv_field = gc_col-vkorg ) )
                      vtweg  = to_upper( get_value( iv_row = lv_row iv_field = gc_col-vtweg ) ) )
        TO mt_row.
    ENDLOOP.

    IF mt_row IS INITIAL.
      RAISE EXCEPTION TYPE lcx_error EXPORTING iv_text = 'Template contains no data rows'.
    ENDIF.
    mo_log->add( iv_type = 'S' iv_text = |Template { lv_file }: { lines( mt_row ) } data row(s) read| ).
  ENDMETHOD.

  METHOD derive_values.
    "PRDHA derived from PRODH_LVL1..n if not given directly
    DATA lv_prdha TYPE string.
    LOOP AT mt_row INTO DATA(ls_row).
      CHECK NOT line_exists( mt_cell[ row = ls_row-row field = gc_col-prdha ] ).
      CLEAR lv_prdha.
      DO gc_prodh_levels TIMES.
        lv_prdha = lv_prdha && get_value( iv_row   = ls_row-row
                                          iv_field = CONV #( |PRODH_LVL{ sy-index }| ) ).
      ENDDO.
      CHECK lv_prdha IS NOT INITIAL.
      INSERT VALUE #( row = ls_row-row field = gc_col-prdha value = lv_prdha ) INTO TABLE mt_cell.
      mo_log->add( iv_type = 'S' is_row = ls_row iv_field = gc_col-prdha
                   iv_text = |Product hierarchy { lv_prdha } derived from PRODH_LVL1-{ gc_prodh_levels }| ).
    ENDLOOP.
  ENDMETHOD.

  METHOD check_columns.
    DATA(lt_ctrl) = lcl_config=>control_columns( ).

    "Columns not maintained in any selected view table
    LOOP AT mt_header INTO DATA(lv_col) WHERE table_line IS NOT INITIAL.
      CHECK NOT line_exists( lt_ctrl[ table_line = lv_col ] ).
      CHECK NOT line_exists( mo_config->mt_fcat[ KEY k_field COMPONENTS temp_field_name = lv_col ] ).
      CHECK lv_col NP 'PRODH_LVL*'.
      mo_log->add( iv_type = 'W' iv_field = lv_col
                   iv_text = 'Column not maintained in the view tables of the selected views - ignored' ).
    ENDLOOP.

    "Mandatory fields that are no column of the template
    LOOP AT mo_config->mt_fcat INTO DATA(ls_fcat) WHERE mandatory = abap_true.
      CHECK NOT line_exists( mt_header[ table_line = ls_fcat-temp_field_name ] ).
      mo_log->add( iv_type = 'W' iv_view = ls_fcat-view iv_field = ls_fcat-temp_field_name
                   iv_fdesc = ls_fcat-description
                   iv_text = 'Mandatory field is not a column of the template' ).
    ENDLOOP.
  ENDMETHOD.

*----------------------------------------------------------------------*
* 5.5 - validation and mapping, row by row
*----------------------------------------------------------------------*
  METHOD validate_and_map.
    LOOP AT mt_row INTO DATA(ls_row).
      DATA(ls_bapi) = VALUE ty_bapi( row = ls_row-row matkey = ls_row-matkey ).

      check_row_control( ls_row ).
      copy_reference( EXPORTING is_row = ls_row CHANGING cs_bapi = ls_bapi ).
      validate_row(   EXPORTING is_row = ls_row CHANGING cs_bapi = ls_bapi ).
      check_existence( is_row = ls_row is_bapi = ls_bapi ).

      "Action specific preparation (rows without errors only)
      IF mo_log->has_error( ls_row-row ) = abap_false.
        CASE lcl_screen=>get_operation( ).
          WHEN gc_op-update.
            prepare_update( EXPORTING is_row = ls_row CHANGING cs_bapi = ls_bapi ).
          WHEN gc_op-extend.
            prepare_extend( EXPORTING is_row = ls_row CHANGING cs_bapi = ls_bapi ).
        ENDCASE.
      ENDIF.

      APPEND ls_bapi TO mt_bapi.
    ENDLOOP.
  ENDMETHOD.

  METHOD check_row_control.
    DATA(lv_opid) = lcl_screen=>get_operation( ).

    "ACTION column must match the action selected on the screen
    DATA(lv_action) = to_upper( get_value( iv_row = is_row-row iv_field = gc_col-action ) ).
    IF lv_action IS NOT INITIAL.
      DATA(lv_row_op) = COND z_de_op_id(
        WHEN lv_action = 'C' OR lv_action = 'CREATE'                        THEN gc_op-create
        WHEN lv_action = 'U' OR lv_action = 'UPDATE' OR lv_action = 'CHANGE' THEN gc_op-update
        WHEN lv_action = 'E' OR lv_action = 'EXTEND'                        THEN gc_op-extend
        ELSE '?' ).
      IF lv_row_op <> lv_opid.
        mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-action
                     iv_text = |Row action '{ lv_action }' does not match the action selected on the screen| ).
      ENDIF.
    ENDIF.

    "MTART / MBRSH in the template must match the selection screen
    DATA(lv_mtart) = to_upper( get_value( iv_row = is_row-row iv_field = gc_col-mtart ) ).
    IF lv_mtart IS NOT INITIAL AND lv_mtart <> p_mtart.
      mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-mtart
                   iv_text = |Material type { lv_mtart } differs from selection { p_mtart }| ).
    ENDIF.
    DATA(lv_mbrsh) = to_upper( get_value( iv_row = is_row-row iv_field = gc_col-mbrsh ) ).
    IF lv_mbrsh IS NOT INITIAL AND lv_mbrsh <> p_indsec.
      mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-mbrsh
                   iv_text = |Industry sector { lv_mbrsh } differs from selection { p_indsec }| ).
    ENDIF.

    "Update / Extend need a material number
    IF lv_opid <> gc_op-create AND lcl_mapper=>is_dummy_key( is_row-matkey ) = abap_true.
      mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-matnr
                   iv_text = 'MATNR is required for Update / Extend' ).
    ENDIF.

    "Reference / copy columns
    IF get_value( iv_row = is_row-row iv_field = gc_col-ref_matnr ) = `` AND
       ( is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_basic ) = abap_true OR
         is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_purch ) = abap_true OR
         is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_mrp   ) = abap_true OR
         is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_sales ) = abap_true OR
         is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_acct  ) = abap_true ).
      mo_log->add( iv_type = 'W' is_row = is_row iv_field = gc_col-ref_matnr
                   iv_text = 'COPY_* flags ignored - no REFERENCE_MATNR given' ).
    ENDIF.
    IF get_value( iv_row = is_row-row iv_field = gc_col-ref_ekorg ) <> ``.
      mo_log->add( iv_type = 'W' is_row = is_row iv_field = gc_col-ref_ekorg
                   iv_text = 'REF_EKORG ignored - purchasing org. data is not part of BAPI_MATERIAL_SAVEREPLICA' ).
    ENDIF.
  ENDMETHOD.

  METHOD copy_reference.
    "Copy the configured fields of the flagged views from the reference
    "material - values given in the template always win
    FIELD-SYMBOLS: <ls_src> TYPE any,
                   <lv_src> TYPE any,
                   <ls_tgt> TYPE any,
                   <lv_tgt> TYPE any.
    CONSTANTS lc_org_keys TYPE string VALUE
      ` MATERIAL MATERIAL_LONG PLANT SALES_ORG DISTR_CHAN VAL_AREA VAL_TYPE STGE_LOC WHSE_NO STGE_TYPE `.
    DATA: lt_views  TYPE tt_views,
          lv_refmat TYPE matnr.

    DATA(lv_ref) = to_upper( get_value( iv_row = is_row-row iv_field = gc_col-ref_matnr ) ).
    CHECK lv_ref IS NOT INITIAL.

    IF is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_basic ) = abap_true.
      INSERT gc_view-basic INTO TABLE lt_views.
    ENDIF.
    IF is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_purch ) = abap_true.
      INSERT gc_view-purch INTO TABLE lt_views.
    ENDIF.
    IF is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_mrp ) = abap_true.
      INSERT gc_view-mrp INTO TABLE lt_views.
    ENDIF.
    IF is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_sales ) = abap_true.
      INSERT gc_view-sales INTO TABLE lt_views.
    ENDIF.
    IF is_flag_set( iv_row = is_row-row iv_field = gc_col-copy_acct ) = abap_true.
      INSERT gc_view-val INTO TABLE lt_views.
    ENDIF.
    CHECK lt_views IS NOT INITIAL.

    CALL FUNCTION 'CONVERSION_EXIT_MATN1_INPUT'
      EXPORTING  input  = lv_ref
      IMPORTING  output = lv_refmat
      EXCEPTIONS OTHERS = 1.
    IF sy-subrc <> 0.
      mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-ref_matnr
                   iv_text = |Invalid reference material { lv_ref }| ).
      RETURN.
    ENDIF.

    TRY.
        DATA(ls_ref) = mo_bapi->get_reference(
          iv_matnr = lv_refmat
          iv_werks = CONV #( to_upper( get_value( iv_row = is_row-row iv_field = gc_col-ref_werks ) ) )
          iv_vkorg = CONV #( to_upper( get_value( iv_row = is_row-row iv_field = gc_col-ref_vkorg ) ) )
          iv_vtweg = CONV #( to_upper( get_value( iv_row = is_row-row iv_field = gc_col-ref_vtweg ) ) ) ).
      CATCH lcx_error INTO DATA(lx_error).
        mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-ref_matnr
                     iv_text = lx_error->get_text( ) ).
        RETURN.
    ENDTRY.

    LOOP AT mo_config->mt_fcat INTO DATA(ls_fcat) WHERE system_derived = abap_false.
      CHECK line_exists( lt_views[ table_line = ls_fcat-view ] ).
      CHECK NOT line_exists( mt_cell[ row = is_row-row field = ls_fcat-temp_field_name ] ).

      LOOP AT ls_fcat-targets INTO DATA(ls_target) WHERE table = abap_false.
        CHECK lc_org_keys NS | { ls_target-comp } |.        "never copy org. keys
        ASSIGN COMPONENT ls_target-param OF STRUCTURE ls_ref TO <ls_src>.
        CHECK sy-subrc = 0.
        ASSIGN COMPONENT ls_target-comp OF STRUCTURE <ls_src> TO <lv_src>.
        CHECK sy-subrc = 0.
        CHECK <lv_src> IS NOT INITIAL.
        ASSIGN COMPONENT ls_target-param OF STRUCTURE cs_bapi TO <ls_tgt>.
        CHECK sy-subrc = 0.
        ASSIGN COMPONENT ls_target-comp OF STRUCTURE <ls_tgt> TO <lv_tgt>.
        CHECK sy-subrc = 0.
        <lv_tgt> = <lv_src>.
        INSERT VALUE #( row = is_row-row field = ls_fcat-temp_field_name ) INTO TABLE mt_copied.
        INSERT ls_fcat-view INTO TABLE cs_bapi-views.
      ENDLOOP.
    ENDLOOP.

    mo_log->add( iv_type = 'S' is_row = is_row iv_field = gc_col-ref_matnr
                 iv_text = |Reference { lv_ref } copied for view(s) { concat_lines_of( table = lt_views sep = `, ` ) }| ).
  ENDMETHOD.

  METHOD validate_row.
    "Step 5.5.1 - one pass over the field catalogue of all selected views
    LOOP AT mo_config->mt_fcat INTO DATA(ls_fcat).
      DATA(lv_value)    = get_value( iv_row = is_row-row iv_field = ls_fcat-temp_field_name ).
      DATA(lv_supplied) = COND abap_bool( WHEN lv_value IS NOT INITIAL THEN abap_true ELSE abap_false ).

      IF ls_fcat-mandatory = abap_true.
        IF lv_supplied = abap_true.
          map_field( EXPORTING is_row = is_row is_fcat = ls_fcat iv_value = lv_value
                     CHANGING  cs_bapi = cs_bapi ).
        ELSEIF is_available( iv_row = is_row-row iv_field = ls_fcat-temp_field_name ) = abap_false.
          mo_log->add( iv_type = 'E' is_row = is_row iv_view = ls_fcat-view
                       iv_field = ls_fcat-temp_field_name iv_fdesc = ls_fcat-description
                       iv_text = |{ ls_fcat-temp_field_name } ({ ls_fcat-description }) is mandatory| ).
        ENDIF.

      ELSEIF ls_fcat-optional = abap_true.
        IF lv_supplied = abap_true.
          map_field( EXPORTING is_row = is_row is_fcat = ls_fcat iv_value = lv_value
                     CHANGING  cs_bapi = cs_bapi ).
        ENDIF.

      ELSEIF ls_fcat-system_derived = abap_true.
        "derived by the system - nothing to do

      ELSEIF ls_fcat-cond_mandatory = abap_true.
        IF lv_supplied = abap_true.
          map_field( EXPORTING is_row = is_row is_fcat = ls_fcat iv_value = lv_value
                     CHANGING  cs_bapi = cs_bapi ).
        ENDIF.
        check_cond_mandatory( is_row      = is_row
                              is_fcat     = ls_fcat
                              iv_supplied = is_available( iv_row   = is_row-row
                                                          iv_field = ls_fcat-temp_field_name ) ).

      ELSE.
        "no flag maintained -> handled like optional
        IF lv_supplied = abap_true.
          map_field( EXPORTING is_row = is_row is_fcat = ls_fcat iv_value = lv_value
                     CHANGING  cs_bapi = cs_bapi ).
        ENDIF.
      ENDIF.
    ENDLOOP.

    "Classification consistency
    LOOP AT cs_bapi-allocvalueschar INTO DATA(ls_char) WHERE charact IS INITIAL.
      mo_log->add( iv_type = 'E' is_row = is_row iv_view = gc_view-class
                   iv_text = |Characteristic value '{ ls_char-value_char }' without characteristic name| ).
    ENDLOOP.
    IF ( cs_bapi-allocvalueschar IS NOT INITIAL OR cs_bapi-allocvaluesnum IS NOT INITIAL OR
         cs_bapi-allocvaluescurr IS NOT INITIAL ) AND cs_bapi-classkey-classnum IS INITIAL.
      mo_log->add( iv_type = 'E' is_row = is_row iv_view = gc_view-class
                   iv_text = 'Characteristic values given, but no class' ).
    ENDIF.
  ENDMETHOD.

  METHOD check_cond_mandatory.
    "ZTMM_COND_MAND: SOURCE_FIELD = this field -> CONDMAT_FIELD required
    LOOP AT mo_config->mt_cond INTO DATA(ls_cond) WHERE source_field = is_fcat-temp_field_name.
      IF gc_cond_if_source = abap_true AND iv_supplied = abap_false.
        CONTINUE.                               "source not maintained -> no check
      ENDIF.
      CHECK is_available( iv_row = is_row-row iv_field = ls_cond-condmat_field ) = abap_false.

      mo_log->add( iv_type  = 'E'
                   is_row   = is_row
                   iv_view  = is_fcat-view
                   iv_field = ls_cond-condmat_field
                   iv_fdesc = ls_cond-condmat_dec
                   iv_text  = |{ ls_cond-condmat_field } ({ ls_cond-condmat_dec }) is mandatory | &&
                              |when { ls_cond-source_field } ({ ls_cond-source_dec }) is maintained| ).
    ENDLOOP.
  ENDMETHOD.

  METHOD map_field.
    "Pass the template value to every BAPI target maintained for the field
    LOOP AT is_fcat-targets INTO DATA(ls_target).
      lcl_mapper=>map_value( EXPORTING is_target = ls_target
                                       iv_field  = is_fcat-temp_field_name
                                       iv_value  = iv_value
                             IMPORTING ev_error  = DATA(lv_error)
                             CHANGING  cs_bapi   = cs_bapi ).
      IF lv_error IS NOT INITIAL.
        mo_log->add( iv_type = 'E' is_row = is_row iv_view = is_fcat-view
                     iv_field = is_fcat-temp_field_name iv_fdesc = is_fcat-description
                     iv_text = lv_error ).
      ENDIF.
    ENDLOOP.
    IF is_fcat-targets IS NOT INITIAL.
      INSERT is_fcat-view INTO TABLE cs_bapi-views.
    ENDIF.
  ENDMETHOD.

  METHOD check_existence.
    TYPES: BEGIN OF lty_org,
             text   TYPE string,
             exists TYPE abap_bool,
           END OF lty_org.
    DATA: lt_org   TYPE STANDARD TABLE OF lty_org WITH EMPTY KEY,
          lv_matnr TYPE matnr,
          lv_dummy TYPE matnr.

    CHECK lcl_mapper=>is_dummy_key( is_row-matkey ) = abap_false.

    CALL FUNCTION 'CONVERSION_EXIT_MATN1_INPUT'
      EXPORTING  input  = is_row-matkey
      IMPORTING  output = lv_matnr
      EXCEPTIONS OTHERS = 1.
    IF sy-subrc <> 0.
      mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-matnr iv_text = 'Invalid material number' ).
      RETURN.
    ENDIF.

    SELECT SINGLE matnr FROM mara INTO @lv_dummy WHERE matnr = @lv_matnr.
    DATA(lv_exists) = COND abap_bool( WHEN sy-subrc = 0 THEN abap_true ELSE abap_false ).
    DATA(lv_opid)   = lcl_screen=>get_operation( ).

    IF lv_opid = gc_op-create.
      IF lv_exists = abap_true.
        mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-matnr
                     iv_text = 'Material already exists - use Update or Extend' ).
      ENDIF.
      RETURN.
    ENDIF.
    IF lv_exists = abap_false.
      mo_log->add( iv_type = 'E' is_row = is_row iv_field = gc_col-matnr
                   iv_text = 'Material does not exist - use Create' ).
      RETURN.
    ENDIF.

    "Org. levels of this row - already maintained for the material?
    IF is_bapi-plantdata-plant IS NOT INITIAL.
      SELECT SINGLE matnr FROM marc INTO @lv_dummy
        WHERE matnr = @lv_matnr AND werks = @is_bapi-plantdata-plant.
      APPEND VALUE #( text   = |Plant { is_bapi-plantdata-plant }|
                      exists = COND #( WHEN sy-subrc = 0 THEN abap_true ELSE abap_false ) ) TO lt_org.
    ENDIF.
    IF is_bapi-salesdata-sales_org IS NOT INITIAL.
      SELECT SINGLE matnr FROM mvke INTO @lv_dummy
        WHERE matnr = @lv_matnr AND vkorg = @is_bapi-salesdata-sales_org
                                AND vtweg = @is_bapi-salesdata-distr_chan.
      APPEND VALUE #( text   = |Sales area { is_bapi-salesdata-sales_org }/{ is_bapi-salesdata-distr_chan }|
                      exists = COND #( WHEN sy-subrc = 0 THEN abap_true ELSE abap_false ) ) TO lt_org.
    ENDIF.
    IF is_bapi-storagelocationdata-stge_loc IS NOT INITIAL.
      DATA(lv_sloc_plant) = COND werks_d( WHEN is_bapi-storagelocationdata-plant IS NOT INITIAL
                                          THEN is_bapi-storagelocationdata-plant
                                          ELSE is_bapi-plantdata-plant ).
      SELECT SINGLE matnr FROM mard INTO @lv_dummy
        WHERE matnr = @lv_matnr AND werks = @lv_sloc_plant
                                AND lgort = @is_bapi-storagelocationdata-stge_loc.
      APPEND VALUE #( text   = |Storage location { lv_sloc_plant }/{ is_bapi-storagelocationdata-stge_loc }|
                      exists = COND #( WHEN sy-subrc = 0 THEN abap_true ELSE abap_false ) ) TO lt_org.
    ENDIF.
    IF is_bapi-valuationdata-val_area IS NOT INITIAL.
      SELECT SINGLE matnr FROM mbew INTO @lv_dummy
        WHERE matnr = @lv_matnr AND bwkey = @is_bapi-valuationdata-val_area
                                AND bwtar = @is_bapi-valuationdata-val_type.
      APPEND VALUE #( text   = |Valuation area { is_bapi-valuationdata-val_area }|
                      exists = COND #( WHEN sy-subrc = 0 THEN abap_true ELSE abap_false ) ) TO lt_org.
    ENDIF.
    IF is_bapi-warehousenumberdata-whse_no IS NOT INITIAL.
      SELECT SINGLE matnr FROM mlgn INTO @lv_dummy
        WHERE matnr = @lv_matnr AND lgnum = @is_bapi-warehousenumberdata-whse_no.
      APPEND VALUE #( text   = |Warehouse { is_bapi-warehousenumberdata-whse_no }|
                      exists = COND #( WHEN sy-subrc = 0 THEN abap_true ELSE abap_false ) ) TO lt_org.
    ENDIF.

    CASE lv_opid.
      WHEN gc_op-update.
        LOOP AT lt_org INTO DATA(ls_org) WHERE exists = abap_false.
          mo_log->add( iv_type = 'E' is_row = is_row
                       iv_text = |{ ls_org-text } does not exist for the material - use Extend| ).
        ENDLOOP.
      WHEN gc_op-extend.
        "existing org. levels are dropped in PREPARE_EXTEND
        IF lt_org IS NOT INITIAL AND NOT line_exists( lt_org[ exists = abap_false ] ).
          mo_log->add( iv_type = 'E' is_row = is_row
                       iv_text = 'Nothing to extend - all org. levels of the row already exist (use Update)' ).
        ENDIF.
    ENDCASE.
  ENDMETHOD.

*----------------------------------------------------------------------*
* Update / Extend
*----------------------------------------------------------------------*
  METHOD prepare_update.
    "UPDATE: compare the template with the current data of the material.
    " - unchanged values are not sent to the BAPI
    " - every changed value is logged as  old -> new
    " - org. levels without any change are dropped
    FIELD-SYMBOLS: <ls_new> TYPE any,
                   <ls_old> TYPE any,
                   <lv_new> TYPE any,
                   <lv_old> TYPE any.
    CONSTANTS:
      lc_params TYPE string VALUE `CLIENTDATA PLANTDATA FORECASTPARAMETERS PLANNINGDATA VALUATIONDATA SALESDATA`,
      lc_keys   TYPE string VALUE ` MATERIAL MATERIAL_LONG FUNCTION PLANT SALES_ORG DISTR_CHAN VAL_AREA VAL_TYPE `.
    DATA: lt_params  TYPE string_table,
          lv_matnr   TYPE matnr,
          lv_changes TYPE i,
          lv_total   TYPE i,
          lv_tfield  TYPE fieldname,
          lv_tdesc   TYPE z_de_field_desc,
          lv_tview   TYPE char10.

    CALL FUNCTION 'CONVERSION_EXIT_MATN1_INPUT'
      EXPORTING  input  = is_row-matkey
      IMPORTING  output = lv_matnr
      EXCEPTIONS OTHERS = 1.
    CHECK sy-subrc = 0.

    plant_defaults( CHANGING cs_bapi = cs_bapi ).

    "Current values for the org. levels of this row
    DATA(lv_plant) = COND werks_d( WHEN cs_bapi-plantdata-plant IS NOT INITIAL
                                   THEN cs_bapi-plantdata-plant
                                   ELSE CONV #( cs_bapi-valuationdata-val_area ) ).
    TRY.
        DATA(ls_cur) = mo_bapi->get_reference( iv_matnr = lv_matnr
                                               iv_werks = lv_plant
                                               iv_vkorg = cs_bapi-salesdata-sales_org
                                               iv_vtweg = cs_bapi-salesdata-distr_chan ).
      CATCH lcx_error INTO DATA(lx_error).
        mo_log->add( iv_type = 'W' is_row = is_row
                     iv_text = |Current values not read ({ lx_error->get_text( ) }) - | &&
                               |all template values are sent| ).
        RETURN.
    ENDTRY.

    SPLIT lc_params AT space INTO TABLE lt_params.
    LOOP AT lt_params INTO DATA(lv_param).
      ASSIGN COMPONENT lv_param OF STRUCTURE cs_bapi TO <ls_new>.
      CHECK sy-subrc = 0.
      CHECK <ls_new> IS NOT INITIAL.
      "valuation data was read for valuation area = plant only
      IF lv_param = `VALUATIONDATA` AND cs_bapi-valuationdata-val_area <> lv_plant.
        CONTINUE.
      ENDIF.
      ASSIGN COMPONENT lv_param OF STRUCTURE ls_cur TO <ls_old>.
      CHECK sy-subrc = 0.

      CLEAR lv_changes.
      DATA(lo_struct) = CAST cl_abap_structdescr( cl_abap_typedescr=>describe_by_data( <ls_new> ) ).
      LOOP AT lo_struct->components INTO DATA(ls_comp).
        CHECK lc_keys NS | { ls_comp-name } |.                  "org. keys stay
        ASSIGN COMPONENT ls_comp-name OF STRUCTURE <ls_new> TO <lv_new>.
        CHECK sy-subrc = 0.
        CHECK <lv_new> IS NOT INITIAL.

        ASSIGN COMPONENT ls_comp-name OF STRUCTURE <ls_old> TO <lv_old>.
        DATA(lv_found) = COND abap_bool( WHEN sy-subrc = 0 THEN abap_true ELSE abap_false ).
        IF lv_found = abap_true AND <lv_new> = <lv_old>.
          CLEAR <lv_new>.                                          "unchanged - not sent
          CONTINUE.
        ENDIF.

        "changed value -> log with template field
        DATA(lv_old_txt) = COND string( WHEN lv_found = abap_true THEN |{ <lv_old> }| ELSE `?` ).
        CLEAR: lv_tfield, lv_tdesc, lv_tview.
        LOOP AT mo_config->mt_fcat INTO DATA(ls_fcat).
          IF line_exists( ls_fcat-targets[ param = lv_param comp = ls_comp-name ] ).
            lv_tfield = ls_fcat-temp_field_name.
            lv_tdesc  = ls_fcat-description.
            lv_tview  = ls_fcat-view.
            EXIT.
          ENDIF.
        ENDLOOP.
        mo_log->add( iv_type  = 'S' is_row = is_row iv_view = lv_tview
                     iv_field = lv_tfield iv_fdesc = lv_tdesc
                     iv_text  = |Change { lv_param }-{ ls_comp-name }: '{ lv_old_txt }' -> '{ <lv_new> }'| ).
        lv_changes = lv_changes + 1.
      ENDLOOP.

      IF lv_changes = 0.
        CLEAR <ls_new>.                     "nothing changed on this org. level
      ENDIF.
      lv_total = lv_total + lv_changes.
    ENDLOOP.

    sync_views( CHANGING cs_bapi = cs_bapi ).

    IF lv_total = 0.
      mo_log->add( iv_type = 'S' is_row = is_row
                   iv_text = 'No differences to the current material data in this row' ).
    ENDIF.
  ENDMETHOD.

  METHOD prepare_extend.
    "EXTEND: only org. levels that do not exist yet are created.
    "Basic data and existing org. levels are not changed (use Update).
    DATA: lv_matnr TYPE matnr,
          lv_dummy TYPE matnr.

    CALL FUNCTION 'CONVERSION_EXIT_MATN1_INPUT'
      EXPORTING  input  = is_row-matkey
      IMPORTING  output = lv_matnr
      EXCEPTIONS OTHERS = 1.
    CHECK sy-subrc = 0.

    plant_defaults( CHANGING cs_bapi = cs_bapi ).

    "Basic data
    IF cs_bapi-clientdata IS NOT INITIAL.
      mo_log->add( iv_type = 'W' is_row = is_row iv_view = gc_view-basic
                   iv_text = 'Basic data ignored - Extend only adds new org. levels (use Update)' ).
      CLEAR cs_bapi-clientdata.
    ENDIF.

    "Plant (incl. MRP / purchasing / forecast / planning data)
    IF cs_bapi-plantdata-plant IS NOT INITIAL.
      SELECT SINGLE matnr FROM marc INTO @lv_dummy
        WHERE matnr = @lv_matnr AND werks = @cs_bapi-plantdata-plant.
      IF sy-subrc = 0.
        mo_log->add( iv_type = 'W' is_row = is_row
                     iv_text = |Plant { cs_bapi-plantdata-plant } already exists - not changed (use Update)| ).
        CLEAR: cs_bapi-plantdata, cs_bapi-forecastparameters, cs_bapi-planningdata.
      ELSE.
        mo_log->add( iv_type = 'S' is_row = is_row
                     iv_text = |Material is extended to plant { cs_bapi-plantdata-plant }| ).
      ENDIF.
    ENDIF.

    "Storage location
    IF cs_bapi-storagelocationdata-stge_loc IS NOT INITIAL.
      SELECT SINGLE matnr FROM mard INTO @lv_dummy
        WHERE matnr = @lv_matnr
          AND werks = @cs_bapi-storagelocationdata-plant
          AND lgort = @cs_bapi-storagelocationdata-stge_loc.
      IF sy-subrc = 0.
        mo_log->add( iv_type = 'W' is_row = is_row
                     iv_text = |Storage location { cs_bapi-storagelocationdata-plant }/| &&
                               |{ cs_bapi-storagelocationdata-stge_loc } already exists - not changed| ).
        CLEAR cs_bapi-storagelocationdata.
      ELSE.
        mo_log->add( iv_type = 'S' is_row = is_row
                     iv_text = |Material is extended to storage location { cs_bapi-storagelocationdata-plant }/| &&
                               |{ cs_bapi-storagelocationdata-stge_loc }| ).
      ENDIF.
    ENDIF.

    "Sales area
    IF cs_bapi-salesdata-sales_org IS NOT INITIAL.
      SELECT SINGLE matnr FROM mvke INTO @lv_dummy
        WHERE matnr = @lv_matnr
          AND vkorg = @cs_bapi-salesdata-sales_org
          AND vtweg = @cs_bapi-salesdata-distr_chan.
      IF sy-subrc = 0.
        mo_log->add( iv_type = 'W' is_row = is_row
                     iv_text = |Sales area { cs_bapi-salesdata-sales_org }/{ cs_bapi-salesdata-distr_chan } | &&
                               |already exists - not changed (use Update)| ).
        CLEAR cs_bapi-salesdata.
      ELSE.
        mo_log->add( iv_type = 'S' is_row = is_row
                     iv_text = |Material is extended to sales area { cs_bapi-salesdata-sales_org }/| &&
                               |{ cs_bapi-salesdata-distr_chan }| ).
      ENDIF.
    ENDIF.

    "Valuation area
    IF cs_bapi-valuationdata-val_area IS NOT INITIAL.
      SELECT SINGLE matnr FROM mbew INTO @lv_dummy
        WHERE matnr = @lv_matnr
          AND bwkey = @cs_bapi-valuationdata-val_area
          AND bwtar = @cs_bapi-valuationdata-val_type.
      IF sy-subrc = 0.
        mo_log->add( iv_type = 'W' is_row = is_row
                     iv_text = |Valuation area { cs_bapi-valuationdata-val_area } already exists - | &&
                               |not changed (use Update)| ).
        CLEAR cs_bapi-valuationdata.
      ELSE.
        mo_log->add( iv_type = 'S' is_row = is_row
                     iv_text = |Material is extended to valuation area { cs_bapi-valuationdata-val_area }| ).
      ENDIF.
    ENDIF.

    "Warehouse number / storage type
    IF cs_bapi-warehousenumberdata-whse_no IS NOT INITIAL.
      SELECT SINGLE matnr FROM mlgn INTO @lv_dummy
        WHERE matnr = @lv_matnr AND lgnum = @cs_bapi-warehousenumberdata-whse_no.
      IF sy-subrc = 0.
        mo_log->add( iv_type = 'W' is_row = is_row
                     iv_text = |Warehouse { cs_bapi-warehousenumberdata-whse_no } already exists - not changed| ).
        CLEAR cs_bapi-warehousenumberdata.
      ENDIF.
    ENDIF.
    IF cs_bapi-storagetypedata-stge_type IS NOT INITIAL.
      SELECT SINGLE matnr FROM mlgt INTO @lv_dummy
        WHERE matnr = @lv_matnr
          AND lgnum = @cs_bapi-storagetypedata-whse_no
          AND lgtyp = @cs_bapi-storagetypedata-stge_type.
      IF sy-subrc = 0.
        mo_log->add( iv_type = 'W' is_row = is_row
                     iv_text = |Storage type { cs_bapi-storagetypedata-whse_no }/| &&
                               |{ cs_bapi-storagetypedata-stge_type } already exists - not changed| ).
        CLEAR cs_bapi-storagetypedata.
      ENDIF.
    ENDIF.

    sync_views( CHANGING cs_bapi = cs_bapi ).

    "Something left to extend?
    IF cs_bapi-plantdata           IS INITIAL AND cs_bapi-storagelocationdata IS INITIAL AND
       cs_bapi-salesdata           IS INITIAL AND cs_bapi-valuationdata       IS INITIAL AND
       cs_bapi-warehousenumberdata IS INITIAL AND cs_bapi-storagetypedata     IS INITIAL AND
       cs_bapi-classkey            IS INITIAL.
      mo_log->add( iv_type = 'E' is_row = is_row
                   iv_text = 'Nothing to extend in this row - no new org. level (use Update)' ).
    ENDIF.
  ENDMETHOD.

  METHOD plant_defaults.
    "Plant of the row for dependent org. level data
    CHECK cs_bapi-plantdata-plant IS NOT INITIAL.
    IF cs_bapi-storagelocationdata IS NOT INITIAL AND cs_bapi-storagelocationdata-plant IS INITIAL.
      cs_bapi-storagelocationdata-plant = cs_bapi-plantdata-plant.
    ENDIF.
    IF cs_bapi-forecastparameters IS NOT INITIAL AND cs_bapi-forecastparameters-plant IS INITIAL.
      cs_bapi-forecastparameters-plant = cs_bapi-plantdata-plant.
    ENDIF.
    IF cs_bapi-planningdata IS NOT INITIAL AND cs_bapi-planningdata-plant IS INITIAL.
      cs_bapi-planningdata-plant = cs_bapi-plantdata-plant.
    ENDIF.
    IF cs_bapi-valuationdata IS NOT INITIAL AND cs_bapi-valuationdata-val_area IS INITIAL.
      cs_bapi-valuationdata-val_area = cs_bapi-plantdata-plant.          "valuation at plant level
    ENDIF.
  ENDMETHOD.

  METHOD sync_views.
    "Views only where data is still sent to the BAPI
    IF cs_bapi-plantdata IS INITIAL.
      DELETE cs_bapi-views WHERE table_line = gc_view-purch.
      IF cs_bapi-forecastparameters IS INITIAL AND cs_bapi-planningdata IS INITIAL.
        DELETE cs_bapi-views WHERE table_line = gc_view-mrp.
      ENDIF.
      IF cs_bapi-storagelocationdata IS INITIAL AND cs_bapi-warehousenumberdata IS INITIAL AND
         cs_bapi-storagetypedata     IS INITIAL.
        DELETE cs_bapi-views WHERE table_line = gc_view-plntst.
      ENDIF.
    ENDIF.
    IF cs_bapi-salesdata IS INITIAL.
      DELETE cs_bapi-views WHERE table_line = gc_view-sales.
    ENDIF.
    IF cs_bapi-valuationdata IS INITIAL.
      DELETE cs_bapi-views WHERE table_line = gc_view-val.
    ENDIF.
    IF cs_bapi-clientdata          IS INITIAL AND cs_bapi-materialdescription IS INITIAL AND
       cs_bapi-unitsofmeasure      IS INITIAL AND cs_bapi-internationalartnos IS INITIAL AND
       cs_bapi-materiallongtext    IS INITIAL AND cs_bapi-taxclassifications  IS INITIAL.
      DELETE cs_bapi-views WHERE table_line = gc_view-basic.
    ENDIF.
  ENDMETHOD.

*----------------------------------------------------------------------*
* Simulation / posting
*----------------------------------------------------------------------*
  METHOD process_materials.
    FIELD-SYMBOLS <ls_class> TYPE ty_bapi.
    DATA: lt_err_mat  TYPE SORTED TABLE OF string WITH UNIQUE KEY table_line,
          lt_seen     TYPE SORTED TABLE OF string WITH UNIQUE KEY table_line,
          lt_mat      TYPE string_table,
          lt_class    TYPE tt_bapi,
          lv_ok_cnt   TYPE i,
          lv_fail_cnt TYPE i,
          lv_skip_cnt TYPE i.

    DATA(lv_mode) = COND string( WHEN p_test = abap_true THEN `Simulation` ELSE `Posting` ).

    "Materials in template order, materials with validation errors
    LOOP AT mt_row INTO DATA(ls_row).
      INSERT ls_row-matkey INTO TABLE lt_seen.
      IF sy-subrc = 0.
        APPEND ls_row-matkey TO lt_mat.
      ENDIF.
      IF mo_log->has_error( ls_row-row ) = abap_true.
        INSERT ls_row-matkey INTO TABLE lt_err_mat.
      ENDIF.
    ENDLOOP.

    LOOP AT lt_mat INTO DATA(lv_matkey).
      DATA(ls_first) = mt_row[ matkey = lv_matkey ].

      IF line_exists( lt_err_mat[ table_line = lv_matkey ] ).
        mo_log->add( iv_type = 'W' is_row = ls_first
                     iv_text = |{ lv_mode } skipped - material has validation errors| ).
        lv_skip_cnt = lv_skip_cnt + 1.
        CONTINUE.
      ENDIF.

      DATA(lv_matnr) = mo_bapi->get_material_number( ls_first ).
      IF lv_matnr IS INITIAL.
        lv_skip_cnt = lv_skip_cnt + 1.
        CONTINUE.
      ENDIF.

      "--- One BAPI_MATERIAL_SAVEREPLICA call per template row:
      "    basic data of the material + org. levels of this row only
      DATA(lv_mat_ok) = abap_true.
      LOOP AT mt_row INTO DATA(ls_mrow) WHERE matkey = lv_matkey.
        DATA(ls_call) = build_call( iv_matkey = lv_matkey
                                    iv_matnr  = lv_matnr
                                    iv_row    = ls_mrow-row ).
        IF lcl_mapper=>has_payload( ls_call ) = abap_false.
          mo_log->add( iv_type = 'S' is_row = ls_mrow
                       iv_text = 'Nothing to change in this row - BAPI not called' ).
          CONTINUE.
        ENDIF.
        IF mo_bapi->save_material( is_call  = ls_call
                                   it_rows  = VALUE #( ( ls_mrow ) )
                                   iv_matnr = lv_matnr ) = abap_false.
          lv_mat_ok = abap_false.
          IF p_test = abap_false.
            mo_log->add( iv_type = 'W' is_row = ls_mrow
                         iv_text = 'Remaining rows of this material not posted after the error' ).
            EXIT.                                   "posting: stop this material
          ENDIF.
        ENDIF.
      ENDLOOP.

      "--- Classification: merged per class over all rows of the material
      CLEAR lt_class.
      LOOP AT mt_bapi INTO DATA(ls_rb) WHERE matkey = lv_matkey.
        CHECK ls_rb-classkey-classnum IS NOT INITIAL.
        READ TABLE lt_class ASSIGNING <ls_class>
             WITH KEY classkey-classnum  = ls_rb-classkey-classnum
                      classkey-classtype = ls_rb-classkey-classtype.
        IF sy-subrc <> 0.
          APPEND VALUE #( classkey = ls_rb-classkey row = ls_rb-row matkey = lv_matkey )
            TO lt_class ASSIGNING <ls_class>.
        ENDIF.
        LOOP AT ls_rb-allocvalueschar INTO DATA(ls_vchar).
          lcl_mapper=>append_unique( EXPORTING is_line = ls_vchar CHANGING ct_tab = <ls_class>-allocvalueschar ).
        ENDLOOP.
        LOOP AT ls_rb-allocvaluesnum INTO DATA(ls_vnum).
          lcl_mapper=>append_unique( EXPORTING is_line = ls_vnum CHANGING ct_tab = <ls_class>-allocvaluesnum ).
        ENDLOOP.
        LOOP AT ls_rb-allocvaluescurr INTO DATA(ls_vcurr).
          lcl_mapper=>append_unique( EXPORTING is_line = ls_vcurr CHANGING ct_tab = <ls_class>-allocvaluescurr ).
        ENDLOOP.
      ENDLOOP.

      "only once the material exists (after posting / for update + extend)
      IF lv_mat_ok = abap_true OR p_test = abap_true.
        LOOP AT lt_class ASSIGNING <ls_class>.
          DATA(ls_crow) = mt_row[ row = <ls_class>-row ].
          IF p_test = abap_true AND lcl_screen=>get_operation( ) = gc_op-create.
            mo_log->add( iv_type = 'W' is_row = ls_crow iv_view = gc_view-class
                         iv_text = |Classification { <ls_class>-classkey-classnum } not simulated - | &&
                                   |material does not exist before posting| ).
            CONTINUE.
          ENDIF.
          IF mo_bapi->classify( is_class = <ls_class> is_row = ls_crow iv_matnr = lv_matnr ) = abap_false.
            lv_mat_ok = abap_false.
          ENDIF.
        ENDLOOP.
      ENDIF.

      IF lv_mat_ok = abap_true.
        lv_ok_cnt = lv_ok_cnt + 1.
      ELSE.
        lv_fail_cnt = lv_fail_cnt + 1.
      ENDIF.
    ENDLOOP.

    mo_log->add( iv_type = COND #( WHEN lv_fail_cnt > 0 THEN 'W' ELSE 'S' )
                 iv_text = |{ lv_mode } finished: { lv_ok_cnt } material(s) successful, | &&
                           |{ lv_fail_cnt } failed, { lv_skip_cnt } skipped| ).
  ENDMETHOD.

  METHOD build_call.
    "One call of BAPI_MATERIAL_SAVEREPLICA for template row IV_ROW:
    " - basic data (header, client data, descriptions, units, texts, tax)
    "   from all rows of the material - every call is complete on its own
    " - org. level data (plant, storage location, sales area, valuation
    "   area, warehouse ...) only from row IV_ROW
    FIELD-SYMBOLS: <ls_src>  TYPE any,
                   <lt_src>  TYPE STANDARD TABLE,
                   <ls_line> TYPE any.
    CONSTANTS:
      lc_single TYPE string VALUE `CLIENTDATA PLANTDATA FORECASTPARAMETERS PLANNINGDATA STORAGELOCATIONDATA VALUATIONDATA WAREHOUSENUMBERDATA SALESDATA STORAGETYPEDATA`,
      lc_tables TYPE string VALUE `MATERIALDESCRIPTION UNITSOFMEASURE INTERNATIONALARTNOS MATERIALLONGTEXT TAXCLASSIFICATIONS`.
    DATA: lt_single TYPE string_table,
          lt_tables TYPE string_table,
          lt_views  TYPE tt_views,
          ls_head   TYPE bapie1mathead.

    SPLIT lc_single AT space INTO TABLE lt_single.
    SPLIT lc_tables AT space INTO TABLE lt_tables.

    LOOP AT mt_bapi INTO DATA(ls_rb) WHERE matkey = iv_matkey.

      "Org. key defaults from the plant of the row
      IF ls_rb-plantdata-plant IS NOT INITIAL.
        IF ls_rb-storagelocationdata IS NOT INITIAL AND ls_rb-storagelocationdata-plant IS INITIAL.
          ls_rb-storagelocationdata-plant = ls_rb-plantdata-plant.
        ENDIF.
        IF ls_rb-forecastparameters IS NOT INITIAL AND ls_rb-forecastparameters-plant IS INITIAL.
          ls_rb-forecastparameters-plant = ls_rb-plantdata-plant.
        ENDIF.
        IF ls_rb-planningdata IS NOT INITIAL AND ls_rb-planningdata-plant IS INITIAL.
          ls_rb-planningdata-plant = ls_rb-plantdata-plant.
        ENDIF.
        IF ls_rb-valuationdata IS NOT INITIAL AND ls_rb-valuationdata-val_area IS INITIAL.
          ls_rb-valuationdata-val_area = ls_rb-plantdata-plant.       "valuation at plant level
        ENDIF.
      ENDIF.

      DATA(lv_this_row) = COND abap_bool( WHEN iv_row IS INITIAL OR ls_rb-row = iv_row
                                          THEN abap_true ELSE abap_false ).

      "Header fields + views with data (org. level views only from this row)
      lcl_mapper=>merge_struct( EXPORTING is_src = ls_rb-headdata CHANGING cs_tgt = ls_head ).
      LOOP AT ls_rb-views INTO DATA(lv_view).
        IF lv_this_row = abap_true OR lv_view = gc_view-basic.
          INSERT lv_view INTO TABLE lt_views.
        ENDIF.
      ENDLOOP.

      "Structures -> table lines: CLIENTDATA from every row, org. levels
      "only from this row
      LOOP AT lt_single INTO DATA(lv_param).
        CHECK lv_this_row = abap_true OR lv_param = `CLIENTDATA`.
        ASSIGN COMPONENT lv_param OF STRUCTURE ls_rb TO <ls_src>.
        CHECK sy-subrc = 0.
        CHECK <ls_src> IS NOT INITIAL.
        lcl_mapper=>add_line( EXPORTING iv_param = CONV #( lv_param )
                                        is_line  = <ls_src>
                                        iv_row   = ls_rb-row
                              CHANGING  cs_call  = rs_call ).
      ENDLOOP.

      "Table parameters of the row
      LOOP AT lt_tables INTO lv_param.
        ASSIGN COMPONENT lv_param OF STRUCTURE ls_rb TO <lt_src>.
        CHECK sy-subrc = 0.
        LOOP AT <lt_src> ASSIGNING <ls_line>.
          lcl_mapper=>add_line( EXPORTING iv_param = CONV #( lv_param )
                                          is_line  = <ls_line>
                                          iv_row   = ls_rb-row
                                CHANGING  cs_call  = rs_call ).
        ENDLOOP.
      ENDLOOP.
    ENDLOOP.

    "Defaults for descriptions and long texts
    LOOP AT rs_call-materialdescription ASSIGNING FIELD-SYMBOL(<ls_makt>)
         WHERE langu IS INITIAL AND langu_iso IS INITIAL.
      <ls_makt>-langu = sy-langu.
    ENDLOOP.
    LOOP AT rs_call-materiallongtext ASSIGNING FIELD-SYMBOL(<ls_text>).
      lcl_mapper=>set_default( EXPORTING iv_comp = 'APPLOBJECT' iv_value = 'MATERIAL' CHANGING cs_line = <ls_text> ).
      lcl_mapper=>set_default( EXPORTING iv_comp = 'TEXT_NAME'  iv_value = iv_matnr   CHANGING cs_line = <ls_text> ).
      lcl_mapper=>set_default( EXPORTING iv_comp = 'TEXT_ID'    iv_value = 'GRUN'     CHANGING cs_line = <ls_text> ).
      lcl_mapper=>set_default( EXPORTING iv_comp = 'LANGU'      iv_value = sy-langu   CHANGING cs_line = <ls_text> ).
    ENDLOOP.

    "Header: type, industry sector, view indicators (screen AND data supplied)
    ls_head-matl_type  = p_mtart.
    ls_head-ind_sector = p_indsec.
    ls_head-basic_view    = COND #( WHEN p_gen   = abap_true AND line_exists( lt_views[ table_line = gc_view-basic  ] ) THEN abap_true ).
    ls_head-purchase_view = COND #( WHEN p_purs  = abap_true AND line_exists( lt_views[ table_line = gc_view-purch  ] ) THEN abap_true ).
    ls_head-mrp_view      = COND #( WHEN p_mrp   = abap_true AND line_exists( lt_views[ table_line = gc_view-mrp    ] ) THEN abap_true ).
    ls_head-storage_view  = COND #( WHEN p_store = abap_true AND line_exists( lt_views[ table_line = gc_view-plntst ] ) THEN abap_true ).
    ls_head-sales_view    = COND #( WHEN p_sales = abap_true AND line_exists( lt_views[ table_line = gc_view-sales  ] ) THEN abap_true ).
    ls_head-account_view  = COND #( WHEN p_acct  = abap_true AND line_exists( lt_views[ table_line = gc_view-val    ] ) THEN abap_true ).
    ls_head-forecast_view  = COND #( WHEN ls_head-mrp_view = abap_true AND rs_call-forecastparameters IS NOT INITIAL
                                     THEN abap_true ).
    ls_head-warehouse_view = COND #( WHEN ls_head-storage_view = abap_true AND rs_call-warehousenumberdata IS NOT INITIAL
                                     THEN abap_true ).
    APPEND ls_head TO rs_call-headdata.

    "Material number in all lines, then the X tables
    lcl_mapper=>set_material_all( EXPORTING iv_matnr = iv_matnr CHANGING cs_call = rs_call ).
    lcl_mapper=>build_x_tables( CHANGING cs_call = rs_call ).
  ENDMETHOD.

*----------------------------------------------------------------------*
* Helpers
*----------------------------------------------------------------------*
  METHOD get_value.
    rv_value = VALUE #( mt_cell[ row = iv_row field = iv_field ]-value OPTIONAL ).
  ENDMETHOD.

  METHOD is_available.
    "value in template or copied from the reference material
    rv_avail = COND #( WHEN line_exists( mt_cell[   row = iv_row field = iv_field ] ) OR
                            line_exists( mt_copied[ row = iv_row field = iv_field ] )
                       THEN abap_true ELSE abap_false ).
  ENDMETHOD.

  METHOD is_flag_set.
    DATA(lv_flag) = to_upper( get_value( iv_row = iv_row iv_field = iv_field ) ).
    rv_set = COND #( WHEN lv_flag = 'X' OR lv_flag = 'Y' OR lv_flag = 'YES' OR
                          lv_flag = '1' OR lv_flag = 'TRUE'
                     THEN abap_true ELSE abap_false ).
  ENDMETHOD.

ENDCLASS.
