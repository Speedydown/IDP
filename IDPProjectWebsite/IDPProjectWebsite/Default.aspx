<%@ Page Title="" Language="C#" MasterPageFile="~/Default.Master" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="IDPProjectWebsite.Default1" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
    <script type="text/javascript">!function (d, s, id) { var js, fjs = d.getElementsByTagName(s)[0]; if (!d.getElementById(id)) { js = d.createElement(s); js.id = id; js.src = "//platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs); } }(document, "script", "twitter-wjs");</script>

</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">

    <div class="balkje">


        <header><h2>Hoe ver zijn we?</h2></header>

        <div class="progress progress-striped active">
            <div class="progress-bar progress-bar-succes" style="width: 18%;"></div>
        </div>
        <div class="progress progress-striped active">
            <div class="progress-bar progress-bar-warning" style="width: 24%;"></div>
        </div>
        <div class="progress progress-striped active">
            <div class="progress-bar progress-bar-danger" style="width: 20%;"></div>
        </div>
        <div class="Legenda">
            <b>Blauw:</b> Informatica: 18% <br />
            <b>Oranje:</b> Elektrotechniek: 24% <br />
            <b>Rood:</b> Werktuigbouwkunde: 20% <br />
        </div>
        
   </div>
    <div class="spacer"></div>
    <div class="balkje">
        <header><h2>Twitter-updates van Tracheata:</h2></header>
        <div class="twitter"> 
        
         <a class="twitter-timeline" href="https://twitter.com/spiderdp" width="520" height="500" data-widget-id="458870517131259904">Tweets van @spiderdp</a>



        </div>
    </div>

    <div class="spacer"></div>
    <div class="balkje">
        <header><h2>Videoupdates van Tracheata</h2></header>
        <div>
        <span>
            <div class="well-lg">
                <iframe width="560" height="315" src="//www.youtube.com/embed/qx4AllfOmsQ?list=PLsnYODr6Xxbbu18I0fVEA8MX87l8-xu9A" frameborder="0" allowfullscreen></iframe>
            </div>
        </span>
        </div>

    </div>


</asp:Content>
