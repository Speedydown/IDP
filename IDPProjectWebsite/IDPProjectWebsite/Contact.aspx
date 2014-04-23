<%@ Page Title="" Language="C#" MasterPageFile="~/Default.Master" AutoEventWireup="true" CodeBehind="Contact.aspx.cs" Inherits="IDPProjectWebsite.Contact" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
    <script type='text/javascript'>
        function winopen(Address) {
            open(Address, "_blank")
        }
    </script>

</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">
    <div class="well-lg">
        <h2>Contact:</h2>
        <div class="contact" onclick="winopen('http://twitter.com/Spiderdp')">
            <div style="position: relative; float: left">
                <asp:Image ID="TwitterImage" runat="server" ImageUrl="/Images/twitter.png" Width="75px" Height="75px" />
            </div>
            <div style="position: relative; float: left; margin-left: 3px;">
                @SpIderDP
            </div>
        </div>
        <div class="contact" onclick="winopen('mailto:riem1203@student.nhl.nl')">
            <div style="position: relative; float: left">
                <asp:Image ID="EmailImage" runat="server" ImageUrl="/Images/email.png" Width="75px" Height="75px" />
            </div>
            <div style="position: relative; float: left; margin-left: 3px;">
                Niels Riemersma <br /> riem1203@student.nhl.nl
            </div>
        </div>
        <div class="contact" onclick="winopen('https://github.com/Speedydown/IDP/')">
            <div style="position: relative; float: left">
                <asp:Image ID="GithubImage" runat="server" ImageUrl="/Images/imagesLCEWID2X.jpg" Width="75px" Height="75px" />
            </div>
            <div style="position: relative; float: left; margin-left: 3px;">
                Github project
            </div>
        </div>
    </div>
</asp:Content>
