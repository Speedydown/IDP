<%@ Page Title="" Language="C#" MasterPageFile="~/Default.Master" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="IDPProjectWebsite.Default1" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
    <script type="text/javascript">!function (d, s, id) { var js, fjs = d.getElementsByTagName(s)[0]; if (!d.getElementById(id)) { js = d.createElement(s); js.id = id; js.src = "//platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs); } }(document, "script", "twitter-wjs");</script>

</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">

    <div class="balkje">

        <header><h2>Hoe ver zijn we?</h2></header>

        <div class="progress progress-striped active">
            <div class="progress-bar progress-bar-succes" style="width: 47%;"></div>
        </div>

        <h3>Recent behaalde doelstellingen:</h3>
        <h4>Week 4:</h4>
        <span>
            Afgelopen week stond onder andere in het teken van de deelfunctiedemo. 
            Bij deze demonstratie heeft het projectteam een aantal functies en tekeningen laten zien aan
            de opdrachtgever. Werktuigbouwkunde heeft de tekeningen van de spin laten zien en Informatica
            heeft onder andere het Vision gedeelte en de pootaansturing via de tablet gedemonstreerd.
            Elektrotechniek heeft de vingerbesturing laten zien.

            Daarnaast heeft Informatica deze week een ontwerpreview gehad welke is afgerond 
            met het oordeel ‘goed’. Elektrotechniek heeft de vingerbesturing draadloos 
            werkend via de Xbee en gewerkt aan de voedingsprintplaat. Werktuigbouwkunde heeft berekeningen 
            gemaakt voor de hoekstanden van de poot en is begonnen met het uitdenken van de spinlift. 
            We hadden deze week één tegenvaller, er zijn twee servo’s kapot gegaan
            tijdens het werken aan het project, dit is opgelost doordat we twee nieuwe servo's gekregen hebben.
        </span>
    </div>

    <div class="spacer"></div>

    <div class="balkje">
        <header><h2>Twitter en YouTube</h2></header>
        <span>
            Onderstaand zijn onze Twitter en YouTube feeds. Hier zal regelmatig een update worden gedeeld vanuit het projectteam.
            Dit kan variëren tussen een projectprestatie of een gezellig moment van het teamproces.
        </span>
    </div>

    
    <div class="balkje">
        <header><h2>Twitter-updates van Tracheata:</h2></header>
        <div class="twitter"> 
        
         <a class="twitter-timeline" href="https://twitter.com/spiderdp" width="520" height="500" data-widget-id="458870517131259904">Tweets van @spiderdp</a>

        </div>
    </div>

    <div class="balkje">
        <header><h2>Videoupdates van Tracheata</h2></header>
        <div>
        <span>
            <iframe width="560" height="315" src="//www.youtube.com/embed/qx4AllfOmsQ?list=PLsnYODr6Xxbbu18I0fVEA8MX87l8-xu9A" frameborder="0" allowfullscreen></iframe>
        </span>
        </div>

    </div>

</asp:Content>
