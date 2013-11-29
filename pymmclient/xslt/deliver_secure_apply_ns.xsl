<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Seal">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/Seal/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery/Header/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery/Header/Sender/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Sender">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery/Message/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery/Message/Header/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery/Message/Header/Supportinfo/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Delivery/Message/Body/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Message">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

</xsl:stylesheet>
