<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="/arg0/Delivery">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Delivery/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Delivery/Header/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Delivery/Message/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Delivery/Message/Header/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Delivery/Message/Header/Supportinfo/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Delivery/Message/Body/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
