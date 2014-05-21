<%@ Page Title="" Language="C#" MasterPageFile="~/Default.Master" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="IDPProjectWebsite.Default1" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
    <script type="text/javascript">!function (d, s, id) { var js, fjs = d.getElementsByTagName(s)[0]; if (!d.getElementById(id)) { js = d.createElement(s); js.id = id; js.src = "//platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs); } }(document, "script", "twitter-wjs");</script>

</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">

    <div class="balkje">

        <header><h2>Hoe ver zijn we?</h2></header>

        <div class="progress progress-striped active">
            <div class="progress-bar progress-bar-succes" style="width: 40%;"></div>
        </div>

        <h3>Recent behaalde doelstellingen:</h3>
        <h4>Week 3:</h4>
        <span>
            Deze week hebben we verschillende deelfuncties gerealiseerd. De communicatie tussen de applicatie 
            en de Raspberry Pi werkt, Elektrotechniek heeft de vingerbesturing werkend en de benodigde
            accu berekend en vrijdag is een prototype van de poot uitgelaserd waarvoor de 
            definitieve tekeningen van Werktuigbouwkunde zijn gebruikt. De vingerbesturing is getest in combinatie
             met de Arduino, momenteel wordt gewerkt aan de communicatie tussen de vingerbesturing en de Raspberry Pi.  
            Deze week is het ook gelukt om de servo’s aan te sturen via de Raspberry Pi, een mooi voorbeeld 
            van samenwerking tussen Informatica en Elektrotechniek. Helaas hadden we op vrijdag te maken met een 
            tegenslag in de vorm van een corrupte SD-kaart waardoor het ons net niet is gelukt om de servo’s aan 
            te sturen via de applicatie.  Donderdag hebben we de ballonnen gekregen, welke ook gebruikt  gaan worden 
            tijdens de wedstrijddag. Deze ballonnen gebruiken we momenteel om onze visiontechnieken te optimaliseren. 
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
