*&---------------------------------------------------------------------*
*& Form get_table_as_csv
*&---------------------------------------------------------------------*
*& Reads all data of a DDIC table, builds a CSV with a header row of
*& data element long texts, and returns it as XSTRING.
*&---------------------------------------------------------------------*
FORM get_table_as_csv
  USING    iv_tabname TYPE tabname
           iv_sep     TYPE c
  CHANGING cv_xstring TYPE xstring.

  DATA lr_data TYPE REF TO data.
  FIELD-SYMBOLS <lt_data> TYPE STANDARD TABLE.

  CLEAR cv_xstring.

  " ---- 1. Check table exists and get its field catalog ----------------
  DATA(lo_struct) = CAST cl_abap_structdescr(
                      cl_abap_typedescr=>describe_by_name( to_upper( iv_tabname ) ) ).
  DATA(lt_dfies)  = lo_struct->get_ddic_field_list( ).

  " ---- 2. Select data into a dynamically typed internal table ---------
  CREATE DATA lr_data TYPE STANDARD TABLE OF (iv_tabname) WITH EMPTY KEY.
  ASSIGN lr_data->* TO <lt_data>.

  SELECT * FROM (iv_tabname) INTO TABLE @<lt_data>.

  " ---- 3. Header row: long text of data element -----------------------
  DATA(lv_sep) = CONV string( iv_sep ).
  DATA(lt_lines) = VALUE string_table( ).

  DATA(lv_header) = concat_lines_of(
    table = VALUE string_table(
              FOR ls_f IN lt_dfies
              ( COND #( WHEN ls_f-scrtext_l IS NOT INITIAL THEN ls_f-scrtext_l
                        WHEN ls_f-fieldtext IS NOT INITIAL THEN ls_f-fieldtext
                        ELSE CONV string( ls_f-fieldname ) ) ) )
    sep   = lv_sep ).
  APPEND lv_header TO lt_lines.

  " ---- 4. Data rows ---------------------------------------------------
  LOOP AT <lt_data> ASSIGNING FIELD-SYMBOL(<ls_row>).
    DATA(lt_cells) = VALUE string_table( ).
    LOOP AT lt_dfies ASSIGNING FIELD-SYMBOL(<ls_f>).
      ASSIGN COMPONENT <ls_f>-fieldname OF STRUCTURE <ls_row> TO FIELD-SYMBOL(<lv_val>).
      IF sy-subrc <> 0.
        APPEND `` TO lt_cells.
        CONTINUE.
      ENDIF.
      " strip separator / line breaks from the value so the CSV stays valid
      DATA(lv_cell) = condense( |{ <lv_val> }| ).
      REPLACE ALL OCCURRENCES OF lv_sep IN lv_cell WITH ` `.
      REPLACE ALL OCCURRENCES OF cl_abap_char_utilities=>cr_lf IN lv_cell WITH ` `.
      REPLACE ALL OCCURRENCES OF cl_abap_char_utilities=>newline IN lv_cell WITH ` `.
      APPEND lv_cell TO lt_cells.
    ENDLOOP.
    APPEND concat_lines_of( table = lt_cells sep = lv_sep ) TO lt_lines.
  ENDLOOP.

  " ---- 5. Build CSV string and convert to XSTRING (UTF-8) -------------
  DATA(lv_csv) = concat_lines_of( table = lt_lines
                                  sep   = cl_abap_char_utilities=>cr_lf ).

  cv_xstring = cl_abap_codepage=>convert_to( source   = lv_csv
                                             codepage = `UTF-8` ).
ENDFORM.
