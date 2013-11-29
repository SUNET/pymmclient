<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="/arg0/SignedDelivery/Signature">
        <xsl:element name="{local-name()}" namespace="http://www.w3.org/2000/09/xmldsig#">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
    <xsl:template match="/arg0/SignedDelivery/Signature/*">
        <xsl:element name="{local-name()}" namespace="http://www.w3.org/2000/09/xmldsig#">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
    <xsl:template match="/arg0/SignedDelivery/Signature/SignedInfo/*">
        <xsl:element name="{local-name()}" namespace="http://www.w3.org/2000/09/xmldsig#">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
    <xsl:template match="/arg0/SignedDelivery/Signature/SignedInfo/Reference/*">
        <xsl:element name="{local-name()}" namespace="http://www.w3.org/2000/09/xmldsig#">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
    <xsl:template match="/arg0/SignedDelivery/Signature/SignedInfo/Reference/Transforms/*">
        <xsl:element name="{local-name()}" namespace="http://www.w3.org/2000/09/xmldsig#">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
    <xsl:template match="/arg0/SignedDelivery/Signature/KeyInfo/*">
        <xsl:element name="{local-name()}" namespace="http://www.w3.org/2000/09/xmldsig#">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
    <xsl:template match="/arg0/SignedDelivery/Signature/KeyInfo/X509Data/*">
        <xsl:element name="{local-name()}" namespace="http://www.w3.org/2000/09/xmldsig#">
            <xsl:apply-templates select="node()|@*" />
        </xsl:element>
    </xsl:template>
    <xsl:template match="/arg0/SignedDelivery/Signature/KeyInfo/X509Data/X509Certificate/text()">
        <xsl:value-of select="translate(.,'&#xA;','')"/>
    </xsl:template>
</xsl:stylesheet>
