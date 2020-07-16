# UDR_prov
Oracle UDR provisioning tool

## Import
example of usage:

$ ./udr_import.py -a create_ent import/import_example.txt.gz

processor
processing import/import_example.txt.gz
file statistics: 
{
 "ENTITLEMENT_NAM1": 1, 
 "ENTITLEMENT_NAM1+ENTITLEMENT_THROT": 3, 
 "ENTITLEMENT_NO_ROAMING": 1, 
 "ENTITLEMENT_THROT": 8
}
processing file is done

importing result will be created inside output directory


## Export
$	./udr_import.py -n -x udr_export_filename.exml.gz

exporting result will be created inside output directory
