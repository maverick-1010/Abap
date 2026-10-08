# Test cases - zom_material_maintenance_v4

Expected results come from reading the code (messages quoted where the code has them). Nothing has been run yet.
Type: P = positive, N = negative. Op: C = Create, U = Update, E = Extend.

## 1. Selection screen and template download

| # | T | Test | Expected |
|---|---|------|----------|
| 1.1 | P | Choose material type, industry sector, business profile, operation, download template | XLSX with one column per field of the active variant + control columns; sheet 2 has legend and field list |
| 1.2 | P | Download template with all view checkboxes ticked | Columns of every selected view (BASIC, CLASS, PURCH, MRP, PLNTST, SALES, VAL) |
| 1.3 | P | Download with only one view ticked | Only that view's columns |
| 1.4 | N | Download without material type / sector / profile | Template has no variant columns (no variant determined) |
| 1.5 | N | No view checkbox ticked | Selection screen rejects execution |
| 1.6 | N | No active variant in ZTMM_MATMAS_MAST for type/sector/profile/operation | Error "No active variant in ZTMM_MATMAS_MAST ...", no posting |
| 1.7 | N | Variant valid_from in the future / valid_to in the past / active_flag blank | Treated as no variant (1.6) |
| 1.8 | P | Two active variants for the same key | First entry is used; run completes |
| 1.9 | N | Selected views have no rows in the view tables | Warning "No fields maintained in ZTMM_xxx_DATA for variant ..." per view; error if no fields at all |

## 2. File upload and template reading

| # | T | Test | Expected |
|---|---|------|----------|
| 2.1 | P | Local file, valid template | Rows read, validation runs |
| 2.2 | P | File on application server (r_unix) | Same as 2.1 |
| 2.3 | N | File path empty or file not found | Error message, nothing posted |
| 2.4 | N | Wrong file format (not XLSX / corrupt) | Error from file reader |
| 2.5 | N | Template with only header rows, no data | Nothing to process / message |
| 2.6 | N | Duplicate column in header | Warning "Duplicate column - first occurrence used" |
| 2.7 | P | Empty cells | Ignored (only non-empty cells are kept) |
| 2.8 | P | Column MESSAGE / ACTION / ROW_NO present | Treated as control columns, not mapped |
| 2.9 | N | Column not in the view tables | Reported as not maintained in config (error per cell) |
| 2.10 | P | MEINS filled | MEINH, UMREZ, UMREN added (1/1) for the base unit |
| 2.11 | P | Leading/trailing spaces in cell values | Trimmed |
| 2.12 | P | Lower case in codes (plant, sales org) | Converted to upper case where the program does so |

## 3. Create

| # | T | Test | Expected |
|---|---|------|----------|
| 3.1 | P | Valid row, MATNR blank, internal numbering | Material created with number from BAPI_MATERIAL_GETINTNUMBER |
| 3.2 | P | Valid row with external MATNR | Created under that number |
| 3.3 | P | Several rows, same MATNR/key (several plants) | One material, one posting per row, basic data merged |
| 3.4 | P | Test run (p_test) | Simulation OK in log, nothing saved |
| 3.5 | N | MATNR already exists | "Material already exists - use Update or Extend" |
| 3.6 | N | MTART in template differs from selection | "Material type X differs from selection Y" |
| 3.7 | N | MBRSH in template differs from selection | "Industry sector X differs from selection Y" |
| 3.8 | N | ACTION column does not match operation | "Row action 'X' does not match the action selected" |
| 3.9 | N | Invalid material number format | "Invalid material number" |
| 3.10 | N | BAPI returns an error | Error in log, rollback, next material still processed |
| 3.11 | N | One row with error, other rows of same material fine | Whole material skipped: "skipped - material has validation errors" |

## 4. Update

| # | T | Test | Expected |
|---|---|------|----------|
| 4.1 | P | Existing material, change a field | Field changed, other fields untouched |
| 4.2 | P | Blank cell for a field | Value left unchanged (no default, no current date) |
| 4.3 | N | MATNR blank | "MATNR is required for Update / Extend" |
| 4.4 | N | Material does not exist | "Material does not exist - use Create" |
| 4.5 | N | Material has another type/sector than the selection | Error with both values |
| 4.6 | N | Plant / sales area / storage location / valuation / warehouse not yet maintained | "<level> does not exist for the material - use Extend" |

## 5. Extend

| # | T | Test | Expected |
|---|---|------|----------|
| 5.1 | P | New plant for an existing material | Plant data created (INS) |
| 5.2 | P | New sales area | Sales data created |
| 5.3 | P | New storage location / valuation area | Created |
| 5.4 | P | Org level already exists | Warning "... already exists - its values will be changed", values updated (UPD) |
| 5.5 | P | Basic data / description / unit / text columns filled | Warning "not changed by Extend - use Update"; ignored |
| 5.6 | N | MATNR blank or material missing | Errors as in 4.3 / 4.4 |
| 5.7 | N | Mandatory client-level field blank | No error (not sent by Extend) |

## 6. Validation, mapping, conversion

| # | T | Test | Expected |
|---|---|------|----------|
| 6.1 | N | Mandatory field blank (column present) | "<FIELD> (<desc>) is mandatory" for that row |
| 6.2 | N | Mandatory field is not a column of the template | "Mandatory field is not a column of the template" |
| 6.3 | P | Mandatory client-level field filled in one of several rows of the same material | No error (row merge) |
| 6.4 | P | Conditional mandatory: source filled, dependent field filled | OK |
| 6.5 | N | Conditional mandatory: source filled, dependent blank | "<FIELD> is mandatory" |
| 6.6 | P | Conditional mandatory: source blank | No check |
| 6.7 | P | Date as YYYYMMDD / Excel serial / user format | Converted to a date |
| 6.8 | N | Invalid date | Error "... rejected ..." |
| 6.9 | P | Number 1,234.50 and 12,5 | Converted correctly |
| 6.10 | N | Text in a number field | Conversion error for that cell |
| 6.11 | P | Field with a conversion exit (ALPHA, CUNIT, MATN1) | Value converted |
| 6.12 | N | Value rejected by conversion exit (e.g. unknown unit) | "Value 'X' rejected by conversion exit ..." |
| 6.13 | P | PRODH_LVL1..5 filled | PRDHA derived, log message |
| 6.14 | P | PRDHA entered directly | Not overwritten |
| 6.15 | N | Value too long for the target field | Error / truncation per field type (check) |
| 6.16 | N | Value for a field whose BAPI structure is not supported | Warning "BAPI structure X not supported - target ignored" |

## 7. Reference material (REFERENCE_MATNR, REF_*, COPY_*)

| # | T | Test | Expected |
|---|---|------|----------|
| 7.1 | P | Reference given, no COPY flags | All selected views copied |
| 7.2 | P | COPY_PURCH = X only | Only purchasing copied |
| 7.3 | P | Template value and reference value for the same field | Template value wins |
| 7.4 | P | Descriptions, units, long texts, tax classifications | Added only for keys not in the template |
| 7.5 | P | Gross weight, volume, dimensions | Copied from reference unit of measure into the template's base unit line |
| 7.6 | P | WERKS / VKORG / VTWEG blank | Taken from REF_WERKS / REF_VKORG / REF_VTWEG, log message |
| 7.7 | P | REF_* blank | Plant / sales area of the template row used |
| 7.8 | N | Reference material does not exist | "Reference material X does not exist" |
| 7.9 | N | Invalid reference number | "Invalid reference material X" |
| 7.10 | N | Reference not maintained in the plant | Error if view requested via COPY flag, warning otherwise; view not copied |
| 7.11 | N | No valuation / sales data for the reference | Same as 7.10 for VAL / SALES |
| 7.12 | N | Reference has another material type | Warning "Reference material has type X - selection is Y" |
| 7.13 | N | COPY_* flag set but REFERENCE_MATNR blank | Error from the row control check |
| 7.14 | P | COPY_BASIC with Extend | Warning "COPY_BASIC ignored - Extend does not change basic data" |
| 7.15 | P | EANs | Never copied |
| 7.16 | N | Base unit of the template differs from the reference | Units not copied, warning |

## 8. Default values (ZTMM_DEFLT_DATA) - Create only

| # | T | Test | Expected |
|---|---|------|----------|
| 8.1 | P | Field blank in template, default exists for type / profile / variant | Default used, log "Value X for FIELD taken from default table" |
| 8.2 | P | Field column not in the template, default exists | Default used |
| 8.3 | P | Template value present | Template value kept, no log |
| 8.4 | P | Value copied from the reference | Reference value kept |
| 8.5 | P | Reference does not fill the field | Default used |
| 8.6 | P | Default for a different type / profile / variant | Not used |
| 8.7 | P | Update and Extend with the same defaults | No default applied |
| 8.8 | P | Two entries for the same field | First one used |
| 8.9 | P | Default for a mandatory field not in the template | No "mandatory" error |
| 8.10 | N | Default for a field not in the variant / selected views | Error "Default for X in ZTMM_DEFLT_DATA: field is not part of variant ..." |
| 8.11 | N | Default for MATNR / WERKS / VKORG / VTWEG or a control column | Error "... not possible - control / key field" |
| 8.12 | N | Default value invalid for the field (wrong format, bad code) | Normal validation error for that field and row |
| 8.13 | P | Default table empty for the selection | Log "0 default value(s)", no change |
| 8.14 | P | Default value 20 characters long | Accepted |

## 9. Current date for VMSTD / MSTDV - Create only

| # | T | Test | Expected |
|---|---|------|----------|
| 9.1 | P | Both blank | Both set to the current date, log message each |
| 9.2 | P | Only one blank | Only that one set |
| 9.3 | P | Value in template | Kept |
| 9.4 | P | Value from default table or reference | Kept |
| 9.5 | P | Column missing from the template, field in the variant | Current date set |
| 9.6 | P | Field not in the variant | Skipped, no error |
| 9.7 | P | Update / Extend | Not applied |
| 9.8 | N | Date set but no status (MSTAE / VMSTA) | Check BAPI behavior |

## 10. Classification

| # | T | Test | Expected |
|---|---|------|----------|
| 10.1 | P | Class and characteristic values, Create | Material posted, then class assigned ("assignment created") |
| 10.2 | P | Update with a characteristic change | Existing assignment changed; other characteristics kept |
| 10.3 | P | Several rows, same class | Values merged, no duplicates |
| 10.4 | P | Class type blank | Default 001 used |
| 10.5 | P | Classification checkbox off | No class columns, no classification |
| 10.6 | N | Characteristic values without a class | "Characteristic values given, but no class" |
| 10.7 | N | Characteristic value without a name | "Characteristic value 'X' without characteristic name" |
| 10.8 | N | Class does not exist / wrong class type | BAPI error, logged, material still saved |
| 10.9 | N | Value not allowed for the characteristic | BAPI error |
| 10.10 | N | Test run with Create | Warning "Classification ... not simulated" |
| 10.11 | N | Two rows with different values for one characteristic | Later value wins, no warning (known behavior) |
| 10.12 | N | Classification fails after the material is saved | Error logged, material remains without class |

## 11. Posting, test run, output

| # | T | Test | Expected |
|---|---|------|----------|
| 11.1 | P | Test run, valid file | Per-material "Simulation OK", rollback |
| 11.2 | P | Posting, valid file | "Posted" per material, commit with wait |
| 11.3 | N | Global error (e.g. no variant) | "Posting not executed - correct the errors first" |
| 11.4 | N | Error in the first row of a material, posting | "Remaining rows ... not posted after the error" |
| 11.5 | N | Commit fails | "Commit failed - ..." |
| 11.6 | P | ALV log | Colours / icons per message type; filter by row, material, field |
| 11.7 | P | Log to application server file / e-mail | File / mail created if selected |
| 11.8 | P | Same message repeated for a row | Shown once |
| 11.9 | N | Material locked by another user | BAPI error, material logged as failed |

## 12. Volume and technical

| # | T | Test | Expected |
|---|---|------|----------|
| 12.1 | P | 1 row | Works |
| 12.2 | P | 1,000 rows / 100 materials | Completes in acceptable time; note run time |
| 12.3 | P | 10,000 rows (log with many messages) | Check run time - log lookups are the known slow spot |
| 12.4 | P | Material with 20+ plants/rows | One material, all org levels created |
| 12.5 | N | Special characters / umlauts / long text | Stored correctly or clean error |
| 12.6 | N | User without authorization for material maintenance | BAPI authorization error in log |
| 12.7 | P | Run twice with the same Create file | Second run: "Material already exists" for external numbers |
