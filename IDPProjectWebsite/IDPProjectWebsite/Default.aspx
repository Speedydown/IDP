<%@ Page Title="" Language="C#" MasterPageFile="~/Default.Master" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="IDPProjectWebsite.Default1" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
    <script type="text/javascript">!function (d, s, id) { var js, fjs = d.getElementsByTagName(s)[0]; if (!d.getElementById(id)) { js = d.createElement(s); js.id = id; js.src = "//platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs); } }(document, "script", "twitter-wjs");</script>

</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">

    <div class="balkje">

        <header><h2>Hoe ver zijn we?</h2></header>

        <div class="progress progress-striped active">
            <div class="progress-bar progress-bar-succes" style="width: 90%;"></div>
        </div>

        <h3>Recent behaalde doelstellingen:</h3>
        <h4>Laatste ontwikkelingen binnen het projectteam</h4>
        <span>
            <br />
            Het is een tijdje geleden sinds ons laatste update rondom het IDP project. Er is gelukkig weer 
            een hoop nieuws te melden, want we hebben de afgelopen week absoluut niet stil gezeten.
            <br />
            <br />
            De spin is inmiddels vrijwel volledig in kleur gespoten en geassembleerd door de Werktuigbouwkunde studenten. 
            De printplaten van Elektrotechniek werken ook en het systeem functioneert naar behoren. Informatica heeft 
            aan de software kant ook de nodige voortgang geboekt.
            <br />
            <br />
            De spin kan alle kanten oplopen en de loopbeweging is ook nog goed gelukt. De constructie van de spin 
            houdt het gewicht van de spin ook goed, dit is goed uitgedacht door de Werktuigbouwkunde studenten. 
            Dit zorgt ervoor dat de servomotoren niet al het gewicht moeten dragen. Elektrotechniek heeft 
            de servomotoren teruggebracht van 7.2v naar 6.0v, dit op aanwijzing van de firma HakDurOos, 
            er waren namelijk meerdere groepen die de servomotoren volledig doorbrandden. Ook op dit voltage kunnen
            we de spin nog goed bewegen en zijn we iets veiliger aan de slag met onze servomotoren.
            <br />
            <br />
            Naast de loopbeweging (hieronder ook in de YouTube-feed te zien) is ook de input van de controller 
            verwerkt in de software en kunnen we nu naast de app op de tablet ook met de controller lopen. 
            Nu de spin volledig gemonteerd is kunnen we ook al de eerste autonome beweging van de spin zien. 
            Met behulp van Vision is al een rode ballon gevolgd.
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
