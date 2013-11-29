<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no"/>

    <xsl:template match="/|comment()|processing-instruction()">
        <xsl:copy>
            <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="*">
        <xsl:element name="{local-name()}">
            <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="@*">
        <xsl:attribute name="{local-name()}">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>

    <!-- Apply our namespace to certain element before signing -->
    <xsl:template match="/SignedDelivery/Delivery/Header/Sender/*">
        <xsl:element name="{local-name()}" namespace="http://minameddelanden.gov.se/schema/Sender">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>

    <!-- Temporary remove certain elements -->
    <!--
    <xsl:template match="/SignedDelivery/Delivery/Message/Header/Reply"/>
    <xsl:template match="/SignedDelivery/Delivery/Message/Header/ReceiptRequest"/>
    -->
    <!-- remove signature element, it will be added by xmlsec -->
    <xsl:template match="/SignedDelivery/Signature"/>
</xsl:stylesheet>
