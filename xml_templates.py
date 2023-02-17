'''

@author: denis
'''

xml_template_subs="""
<txRequest id="1">
<createSubscriber>
<key>
<MSISDN>{KEY}</MSISDN>
</key>
<entity>
<data>
<name>Subscriber</name>
<interface>XMLIMPORT</interface>
<xpath/>
</data>
<content>
<![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<subscriber>
<field name="MSISDN">{KEY}</field>
</subscriber>
]]>
</content>
</entity>
</createSubscriber>
</txRequest>
""".replace("\n", "")

xml_template_state="""
<txRequest id="2">
<create createEntityIfNotExist="true">
<key>
<MSISDN>{KEY}</MSISDN>
</key>
<entity>
<data>
<name>State</name>
<interface>XMLIMPORT</interface>
<xpath/>
</data>
<content>
<![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<state>
<version>1</version>
<property>
<name>status</name>
<value>default</value>
</property>
</state>
]]>
</content>
</entity>
</create>
</txRequest>
""".replace("\n", "")

xml_template_subs_and_state="<transaction>"+xml_template_subs+xml_template_state+"</transaction>"

# Delete subscribers
xml_template_delete_subs="""
<deleteSubscriber>
<key>
<MSISDN>{KEY}</MSISDN>
</key>
</deleteSubscriber>
""".replace("\n", "")

# Delete state
xml_template_delete_state="""
<deleteFieldSet>
<key>
<MSISDN>{KEY}</MSISDN>
</key>
<entity>
<data>
<name>State</name>
<interface>XMLIMPORT</interface>
<xpath/>
</data>
</entity>
</deleteFieldSet>
""".replace("\n", "")

# Create subs with MSISDN
xml_template_subs_with_ent="""
<createSubscriber>
<key>
<MSISDN>{KEY}</MSISDN>
</key>
<entity>
<data>
<name>Subscriber</name>
<interface>XMLIMPORT</interface>
<xpath/>
</data>
<content>
<![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<subscriber>
<field name="MSISDN">{KEY}</field>
<field name="Entitlement">{Entitlement}</field>
</subscriber>
]]>
</content>
</entity>
</createSubscriber>
""".replace("\n", "")

# Update subs field with MSISDN
xml_template_field_update="""
<updateField clearAll="false">
<key>
<MSISDN>{KEY}</MSISDN>
</key>
<entity>
<data>
<name>Subscriber</name>
<interface>XMLIMPORT</interface>
<xpath>/subscriber</xpath>
</data>
<fields>
<field name="Entitlement">{Entitlement}</field>
</fields>
</entity>
</updateField>
""".replace("\n", "")


xml_template_replace_subs_and_end="<transaction><txRequest id=\"1\">"+xml_template_delete_subs+"</txRequest><txRequest id=\"2\">"+xml_template_subs_with_ent+"</txRequest></transaction>"

xml_template=dict()

xml_template = {
    'delete' : xml_template_delete_subs
    ,'create_state' : xml_template_subs_and_state
    ,'create_ent' : xml_template_subs_with_ent
    ,'replace_ent': xml_template_replace_subs_and_end
    ,'delete_state' : xml_template_delete_state
    ,'update_field' : xml_template_field_update
    ,'create' : xml_template_subs
    }
