<xsl:template match="data">
<xsl:variable name="THIS" select="." />
<xsl:variable name="BOTH" select="a/item | b/item" />
    <xsl:for-each select="$BOTH[(position() &lt;= count($THIS/a/item)) or (position() &lt;= count($THIS/b/item))]">
        <xsl:variable name="INDEX" select="position()" />
        <tr>
            <td>
                <xsl:value-of select="$INDEX" />
            </td>
            <td>
                <xsl:choose>
                    <xsl:when test="$INDEX &lt;= count($THIS/a/item)">
                        <xsl:apply-templates select="$THIS/a/item[$INDEX]" />
                    </xsl:when>
                    <xsl:otherwise>
                        -
                    </xsl:otherwise>
                </xsl:choose>
            </td>
            <td>
                <xsl:choose>
                    <xsl:when test="$INDEX &lt;= count($THIS/b/item)">
                        <xsl:apply-templates select="$THIS/b/item[$INDEX]" />
                    </xsl:when>
                    <xsl:otherwise>
                        -
                    </xsl:otherwise>
                </xsl:choose>
            </td>
        </tr>
    </xsl:for-each>
