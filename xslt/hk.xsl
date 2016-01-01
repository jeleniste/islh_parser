<xsl:stylesheet version="1.0"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:cis="http://ciselniky"
   > 
<xsl:param name="ODD"/>
<xsl:param name="DIL"/>
<xsl:param name="POR"/>
<xsl:param name="PSK"/>
<xsl:template match='LHC'>


<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta content="text/html; charset=utf-8" />
<title>Hospodářská kniha</title>
<style>
h2{
  background-color: #DDD; 
  margin-bottom: 0px;
  margin-left: 2px;
  margin-right: 2px;
  margin-top: 5px;
  padding-left: 20px;
  padding-top: 8px;
  padding-bottom: 4px;
  font-family:Helvetica;
  font-size: 95%;
}

table {
   /*border-collapse: collapse;*/
   width: 100%;
   font-family:Helvetica;
   font-size:80%;
}

table.lhc {
   border-collapse: collapse;
   width:350px;
}

th, td {
    padding: 3px;
    padding-left: 5px;
}
div.rotate {
   -webkit-transform: rotate(270deg);
   -moz-transform: rotate(270deg);
   -ms-transform: rotate(270deg);
   -o-transform: rotate(270deg);
   transform: rotate(270deg);
   transform: rotate(270deg);
   vertical-align: bottom;
}

th.rotate {
   vertical-align: center;
}

td.empty {
   background-color:#FFF;
}

th {
    background-color: #AAA;
    color: white;
    vertical-align: center;
    text-align: center;
}
th.field-name{
   text-align: left;
   background-color: #343;
}

tfoot td{
    background-color: #AAA;
    color: white;
    font-weight: bold;
}

div.dreviny{
   margin-left:25px;
}

div.porostni-skupina{
   margin-left:15px;
}
div.porost{
   margin-left:15px;
}

div.etaz{
   margin-top:5px;
}

table.lhc td {
   padding-bottom:1px;
   padding-top:1px;
}

table.por th, td {
   vertical-align:top;
}

table.psk th, td {
   vertical-align:top;
}

tr{background-color: #DDD}

</style>
</head>
<body>
   <div id="hospodarska-kniha">
      <table class="lhc">
	 <colgroup>
	    <col width="22%"/>
	    <col width="78%"/>
	 </colgroup>
	 <tbody>
	    <tr>
	       <th class="field-name">Kód LHC:</th>
	       <td class="field-body"><strong><xsl:value-of select='@LHC_KOD'/></strong></td>
	    </tr>
	    <tr>
	       <th class="field-name">LS(LZ):</th>
	       <td class="field-body"><strong><xsl:value-of select='@LHC_NAZ'/></strong></td>
	    </tr>
	    <tr>
	       <th class="field-name">Platnost:</th>
	       <td class="field-body"><strong><xsl:value-of select='@LHP_OD'/> - <xsl:value-of select='@LHP_DO'/></strong></td>
	    </tr>
	 </tbody>
      </table>
   </div>
   <xsl:apply-templates select="ODD[@ODD=$ODD]/DIL[@DIL=$DIL]/POR[@POR=$POR]"/>
</body>
</html>
</xsl:template>

<xsl:template match='POR'>
   <div class="porost">
      <table class="por">
	 <colgroup>
	    <col width="15%"/>
	    <col width="10%"/>
	    <col width="15%"/>
	    <col width="20%"/>
	    <col width="20%"/>
	    <col width="20%"/>
	 </colgroup>
	 <tbody>
	    <tr>
	       <td>Oddělení: <strong><xsl:value-of select='../../@ODD'/></strong></td>
	       <td>plocha: <strong><xsl:value-of select= 'sum(../../DIL/POR/PSK/@PSK_P)'/></strong></td>
	       <td>Dílec: <strong><xsl:value-of select='../@DIL'/></strong></td>
	       <td>plocha: <strong><xsl:value-of select= 'sum(../POR/PSK/@PSK_P)'/></strong></td>
	       <td>Porost: <strong><xsl:value-of select='@POR'/></strong></td>
	       <td>plocha: <strong><xsl:value-of select= 'sum(PSK/@PSK_P)'/></strong></td>
	    </tr>
	    <tr>
	       <td colspan="3">Lesní oblast: <strong><xsl:value-of select='@LES_OBL'/>
		     <xsl:text> -  </xsl:text>
		     <xsl:value-of select='cis:lesni_oblast(string(@LES_OBL))'/>
	       </strong></td>
	       <td>OLH: <strong><xsl:value-of select='@OLH'/></strong></td>
	       <td colspan="2">Pásmo ohrožení: <strong><xsl:value-of select = '@PAS_OHR'/></strong></td>
	    </tr>
	    <tr>
	       <td colspan="3">Majetek: <strong><xsl:value-of select='@MAJ_DRUH'/>/<xsl:value-of select='@MAJ_KOD'/></strong></td>
	       <td colspan="3">Zvl. statut: <strong><xsl:value-of select='cis:zvl_statut(string(@ZVL_STATUT))'/></strong></td>
	    </tr>
	    <tr>
	       <td colspan="3">kategorie:<br/><xsl:apply-templates select='KAT'/></td>
	       <td colspan="3">Popis porostu:<br/><xsl:value-of select='@POR_TEXT'/></td>
	    </tr>
	 </tbody>
      </table>
   </div>
   <xsl:apply-templates select='PSK[@PSK=$PSK]'/>
</xsl:template>
<xsl:template match='PSK'>
   <div class="porostni-skupina">
      <h2>Porostní skupina</h2>
      <table class="psk">
	 <colgroup>
	    <col width="15%" />
	    <col width="15%" />
	    <col width="10%" />
	    <col width="50%" />
	 </colgroup>
	 <tbody>
	    <tr>
	       <td>PSK: <strong><xsl:value-of select='@PSK'/></strong></td>
	       <td>Plocha: <strong><xsl:value-of select='@PSK_P'/></strong></td>
	       <td colspan="2">Lesní typ: <strong>
		     <xsl:value-of select='cis:slt(string(@SLT))'/>
		     /
		     <xsl:value-of select='@LT'/>
	       </strong></td>
	    </tr>
	    <tr>
	       <td colspan="3">KU: <strong><xsl:value-of select='@KATUZE_KOD'/> 
		     /
		     <xsl:value-of select='cis:katuze(string(@KATUZE_KOD))'/></strong></td>
	       <td>Lesní vegetační stupeň: <strong><xsl:value-of select='cis:lvs(string(@LVS))'/></strong></td>
	    </tr>
	    <tr>
	       <td colspan="4">Popis psk: <xsl:value-of select='@PSK_TEXT'/></td>
	    </tr>
	 </tbody>
      </table>
      <xsl:apply-templates select='ETZ'/>
   </div>
</xsl:template>
<xsl:template match='ETZ'>
      <div class="etaz">
	 <table class="etaz">
	    <colgroup>
	       <col width="8%" />
	       <col width="18%" />
	       <col width="26%" />
	       <col width="26%" />
	       <col width="22%" />
	    </colgroup>
	    <tbody>
	       <tr>
		  <td>Etáž:<br/><strong><xsl:value-of select='@ETAZ'/></strong></td>
		  <td>Parc. / Skut. plocha:<br/><strong><xsl:value-of select='@ETAZ_PP'/>
			/
			<xsl:value-of select='@ETAZ_PS'/></strong></td>
		  <td>Model. těž. %:<br/><strong><xsl:value-of select='@M_TEZ_PROC'/></strong></td>
		  <td>Obmýtí/Obnov.doba:<br/><strong><xsl:value-of select='@OBMYTI'/>
			/
			<xsl:value-of select='@OBN_DOBA'/></strong></td>
		  <td>% mel. a zpevn. drev.:<br/><strong><xsl:value-of select='@MZD'/></strong></td>
	       </tr>
	    </tbody>
	 </table>
	 <div class="dreviny" style="overflow-x:auto;">
	    <table class="dreviny">
	       <thead>
		  <tr>
		     <th rowspan="2"><div class="rotate">Hospodářský<br/>soubor</div></th>
		     <th rowspan="2"><div class="rotate">Věk</div></th>
		     <th rowspan="2"><div class="rotate">Zakmenění</div></th>
		     <th rowspan="2"><div class="rotate">Dřevina</div></th>
		     <th rowspan="2"><div class="rotate">Zastoupení<br/>%</div></th>
		     <th rowspan="2"><div class="rotate">Výpočetní<br/>tlouštka<br/>cm</div></th>
		     <th rowspan="2"><div class="rotate">Výška<br/>m</div></th>
		     <th rowspan="2"><div class="rotate">Objem<br/>středního<br/>kmene</div></th>
		     <th rowspan="2"><div class="rotate">Bonita<br/>absolutní</div></th>
		     <th rowspan="2"><div class="rotate">Bonita<br/>relativní</div></th>
		     <th rowspan="2"><div class="rotate">Genetická<br/>klasifikace</div></th>
		     <th colspan="2">Poškození</th>
		     <th rowspan="2"><div class="rotate">Imise</div></th>
		     <th rowspan="2"><div class="rotate">%<br/>Souší</div></th>
		     <th colspan="2">Zásoba<br/>v m<sup>3</sup> b.k.</th>
		     <th colspan="4">Těžba výchovná</th>
		     <th colspan="2">Těžba<br/>obnovní</th>
		     <th colspan="3">Prořezávky</th>
		     <th colspan="4">Zalesnění</th>
		  </tr>
		  <tr>
		     <th>Druh</th>
		     <th>%</th>
		     <th>na<br/>1 ha</th>
		     <th>celkem</th>
		     <th>naléhavost</th>
		     <th>násobnost</th>
		     <th>plocha<br/>ha</th>
		     <th>objem<br/>m<sup>3</sup></th>
		     <th>plocha<br/>ha</th>
		     <th>objem<br/>m<sup>3</sup></th>
		     <th>naléhavost</th>
		     <th>násobnost</th>
		     <th>plocha<br/>ha</th>
		     <th>Dřevina</th>
		     <th>Druh</th>
		     <th>Zastoupení<br/>%</th>
		     <th>Plocha<br/>ha</th>
		  </tr>
	       </thead>
	       <tbody>
		  <xsl:variable name="THIS" select="." />
		  <xsl:variable name="BOTH" select="DRV | ZAL" />
		  <xsl:variable name="RWSPN">
		     <xsl:choose>
			<xsl:when test="count(DRV) > count(ZAL)">
			   <xsl:value-of select="count(DRV)"/>
			</xsl:when>
			<xsl:otherwise>
			   <xsl:value-of select="count(ZAL)"/>
			</xsl:otherwise>
		     </xsl:choose>
		  </xsl:variable>
		  <xsl:for-each select="$BOTH[(position() &lt;= count($THIS/DRV)) or (position() &lt;= count($THIS/ZAL))]">
		     <xsl:variable name="INDEX" select="position()" />
		     <tr>
			<xsl:if test='$INDEX = 1'>
			   <td>
			      <xsl:attribute name="rowspan">
				 <xsl:value-of select='$RWSPN'/>
			   </xsl:attribute><xsl:value-of select='../@HS'/></td>
			   <td>
			      <xsl:attribute name="rowspan">
				 <xsl:value-of select='$RWSPN'/>
			   </xsl:attribute><xsl:value-of select='../@VEK'/></td>
			   <td>
			      <xsl:attribute name="rowspan">
				 <xsl:value-of select='$RWSPN'/>
			   </xsl:attribute><xsl:value-of select='../@ZAKM'/></td>
			</xsl:if>
			<xsl:choose>
			   <xsl:when test="$INDEX &lt;= count($THIS/DRV)">
			      <xsl:apply-templates select="$THIS/DRV[$INDEX]">
				 <xsl:with-param name="INDEX" select="$INDEX" tunnel="yes"/>
			      </xsl:apply-templates>
			   </xsl:when>
			   <xsl:otherwise>
			      <td class="empty" colspan="23"/>
			   </xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
			   <xsl:when test="$INDEX &lt;= count($THIS/ZAL)">
			      <xsl:apply-templates select="$THIS/ZAL[$INDEX]">
				 <xsl:with-param name="INDEX" select="$INDEX" tunnel="yes"/>
			      </xsl:apply-templates>
			   </xsl:when>
			   <xsl:otherwise>
			      <td class="empty" colspan="4"/>
			   </xsl:otherwise>
			</xsl:choose>
		     </tr>
		  </xsl:for-each>
	       </tbody>
	       <tfoot>
		  <tr>
		     <td colspan="4">Etáž celkem</td>
		     <td><xsl:value-of select='sum(DRV/@ZAST)'/></td>
		     <td colspan="10"></td>
		     <td><xsl:value-of select='sum(DRV/@DR_ZAS_HA)'/></td>
		     <td><xsl:value-of select='sum(DRV/@DR_ZAS_CEL)'/></td>
		     <td colspan="2"></td>
		     <td><xsl:value-of select='@TV_P'/></td>
		     <td><xsl:value-of select='sum(DRV/@DR_TV)'/></td>
		     <td><xsl:value-of select='@TO_P'/></td>
		     <td><xsl:value-of select='sum(DRV/@DR_TO)'/></td>
		     <td colspan="2"></td>
		     <td><xsl:value-of select='@PRO_P'/></td>
		     <td colspan="2"></td>
		     <td><xsl:value-of select='sum(ZAL/@ZAL_DR_P)'/></td>
		     <td><xsl:value-of select='@ZAL_P'/></td>
		  </tr>
		  <xsl:if test="not(following-sibling::ETZ)">
		     <tr>
			<xsl:choose>
			   <xsl:when test='DRV'>
			      <td colspan="4">Porostní skupina celkem</td>
			      <td colspan="11"></td>
			      <td><xsl:value-of select='sum(../ETZ/DRV/@DR_ZAS_HA)'/></td>
			      <td><xsl:value-of select='sum(../ETZ/DRV/@DR_ZAS_CEL)'/></td>
			      <td colspan="2"></td>
			      <td><xsl:value-of select='sum(../ETZ/@TV_P)'/></td>
			      <td><xsl:value-of select='sum(../ETZ/DRV/@DR_TV)'/></td>
			      <td><xsl:value-of select='sum(../ETZ/@TO_P)'/></td>
			      <td><xsl:value-of select='sum(../ETZ/DRV/@DR_TO)'/></td>
			      <td colspan="2"></td>
			      <td><xsl:value-of select='sum(../ETZ/@PRO_P)'/></td>
			   </xsl:when>
			   <xsl:otherwise>
			      <td class="empty" rowspan="23"/>
			   </xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
			   <xsl:when test='ZAL'>
			      <td colspan="2"></td>
			      <td><xsl:value-of select='sum(../ETZ/ZAL/@ZAL_DR_P)'/></td>
			      <td><xsl:value-of select='sum(../ETZ[@ZAL_P !=""]/@ZAL_P)'/></td>
			   </xsl:when>
			   <xsl:otherwise>
			      <td class="empty" rowspan="4"/>
			   </xsl:otherwise>
			</xsl:choose>
		     </tr>
		  </xsl:if>
	       </tfoot>
	    </table>
	 </div>
      </div>
</xsl:template>
<xsl:template match='DRV'>
		     <xsl:param name="INDEX" tunnel="yes"/>
		     <xsl:variable name="RWSPN" select="count(../DRV)"/>
		     <td><xsl:value-of select='@DR_ZKR'/></td>
		     <td><xsl:value-of select='@ZAST'/></td>
		     <td><xsl:value-of select='@TLOUSTKA'/></td>
		     <td><xsl:value-of select='@VYSKA'/></td>
		     <td><xsl:value-of select='@HMOT'/></td>
		     <td><xsl:value-of select='@BON_A'/></td>
		     <td><xsl:value-of select='@BON_R'/></td>
		     <td><xsl:value-of select='@GEN_KLAS'/></td>
		     <xsl:choose>
			<xsl:when test='POS'>
			   <td>
			      <xsl:for-each select='POS'>
				 <xsl:if test='position() !=1'><br/></xsl:if>
				 <xsl:value-of select='@POSKOZ_D'/>
			      </xsl:for-each>
			   </td>
			   <td>
			      <xsl:for-each select='POS'>
				 <xsl:if test='position() !=1'><br/></xsl:if>
				 <xsl:value-of select='@POSKOZ_R'/>
			      </xsl:for-each>
			   </td>
			</xsl:when>
			<xsl:otherwise>
			   <td/>
			   <td/>
			</xsl:otherwise>
		     </xsl:choose>
		     <!--td class="empty"/><xsl:value-of select='@'/>${D} neni v datech, nemam podle ceho udelat</td-->
		     <!--td class="empty"/><xsl:value-of select='@'/>$ neni v datech, nemam podle ceho udelat</td-->
		     <td><xsl:value-of select='@IMISE'/></td>
		     <td><xsl:value-of select='@PROC_SOUS'/></td>
		     <td><xsl:value-of select='@DR_ZAS_HA'/></td>
		     <td><xsl:value-of select='@DR_ZAS_CEL'/></td>
		     <xsl:if test='$INDEX=1'>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@TV_NAL'/></td>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@TV_POC'/></td>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@TV_P'/></td>
		     </xsl:if>
		     <td><xsl:value-of select='@DR_TV'/></td>
		     <xsl:if test='$INDEX=1'>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@TO_P'/></td>
		     </xsl:if>
		     <td><xsl:value-of select='@DR_TO'/></td>
		     <xsl:if test='$INDEX=1'>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@PRO_NAL'/></td>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@PRO_POC'/></td>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@PRO_P'/></td>
		     </xsl:if>
</xsl:template>
<xsl:template match='ZAL'>
		     <xsl:param name="INDEX" tunnel="yes"/>
		     <xsl:variable name="RWSPN" select="count(../ZAL)"/>
		     <td><xsl:value-of select='@ZAL_DR'/></td>
		     <xsl:if test='$INDEX=1'>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@ZAL_DRUH'/></td>
		     </xsl:if>
		     <td><xsl:value-of select='@ZAL_DR_P'/></td>
		     <xsl:if test='$INDEX=1'>
			<td>
			   <xsl:attribute name="rowspan"><xsl:value-of select="$RWSPN"/></xsl:attribute>
			   <xsl:value-of select='../@ZAL_P'/></td>
		     </xsl:if>
</xsl:template>
<xsl:template match='KAT'>
   <xsl:value-of select='@KATEGORIE'/> - 
   <xsl:choose>
      <xsl:when test="@KATEGORIE = '10'">lesy, které nejsou zařazeny v kategorii lesů ochranných nebo lesů zvláštního určení</xsl:when>
      <xsl:when test="@KATEGORIE = '21a'">lesy na mimořádně nepříznivých stanovištích</xsl:when>
      <xsl:when test="@KATEGORIE = '21b'">vysokohorské lesy pod hranicí stromové vegetace chránící níže položené lesy a lesy na exponovaných hřebenech</xsl:when>
      <xsl:when test="@KATEGORIE = '21c'">lesy v klečovém lesním vegetačním stupni</xsl:when>
      <xsl:when test="@KATEGORIE = '31a'">lesy v pásmu hygienické ochrany vodních zdrojů I.stupně</xsl:when>
      <xsl:when test="@KATEGORIE = '31b'">lesy v ochranném pásmu zdrojů přírodních léčivých a stolních minerálních vod</xsl:when>
      <xsl:when test="@KATEGORIE = '31c'">lesy na území nár. parků a nár.přírodních rezervací</xsl:when>
      <xsl:when test="@KATEGORIE = '32a'">lesy v 1.zónách CHKO, lesy v přír. rezervacích a přírodních památkách</xsl:when>
      <xsl:when test="@KATEGORIE = '32b'">lázeňské lesy</xsl:when>
      <xsl:when test="@KATEGORIE = '32c'">příměstské a další lesy se zvýšenou funkcí rekreační</xsl:when>
      <xsl:when test="@KATEGORIE = '32d'">lesy sloužící lesnickému výzkumu a lesnické výuce</xsl:when>
      <xsl:when test="@KATEGORIE = '32e'">lesy se zvýšenou funkcí půdoochrannou, vodoochrannou, klimatickou nebo krajinotvornou</xsl:when>
      <xsl:when test="@KATEGORIE = '32f'">lesy pro zachování biologické různorodosti</xsl:when>
      <xsl:when test="@KATEGORIE = '32g'">lesy v uznaných oborách a samostatných bažantnicích</xsl:when>
      <xsl:when test="@KATEGORIE = '32h'">lesy v nichž jiný důležitý veřejný zájem vyžaduje odlišný způsob hospodaření</xsl:when>
   </xsl:choose>
   <br/>
</xsl:template>
</xsl:stylesheet>
