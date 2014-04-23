<%@ Page Title="" Language="C#" MasterPageFile="~/Default.Master" AutoEventWireup="true" CodeBehind="WeZijnWe.aspx.cs" Inherits="IDPProjectWebsite.WeZijnWe" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">

        <div class="balkje">
            <span>
                <h2> Project leden:</h2>
            </span>
        </div>
        

        <asp:Repeater ID="InformaticaRepeater" runat="server">
            <HeaderTemplate>
                <div class="well-lg">
                    <span>
                        <h3>Informatica:</h3>
                    </span>
                </div>
            </HeaderTemplate>
            <ItemTemplate> 
                <div class="media balkje">                
                    <a class="pull-left" href="#">
                        <img class="media-object" src="<%# Eval("Plaatje") %>">
                    </a>
                    <div class="media-body">
                        <h4 class="media-heading"><b><%# Eval("Voornaam") + " " + Eval("Achternaam") %></b></h4>
                        <%# Eval("Beschrijving") %>
                    </div>
                </div>
            </ItemTemplate>
            <FooterTemplate>
                
            </FooterTemplate>
        </asp:Repeater>

    <asp:Repeater ID="WTBRepeater" runat="server">
            <HeaderTemplate>
                <div class="well-lg">
                    <span>
                        <h3>Werktuigbouwkunde:</h3>
                    </span>
                </div>
            </HeaderTemplate>
            <ItemTemplate> 
                <div class="media balkje">                
                    <a class="pull-left" href="#">
                        <img class="media-object" src="<%# Eval("Plaatje") %>">
                    </a>
                    <div class="media-body">
                        <h4 class="media-heading"><b><%# Eval("Voornaam") + " " + Eval("Achternaam") %></b></h4>
                        <%# Eval("Beschrijving") %>
                    </div>
                </div>
            </ItemTemplate>
            <FooterTemplate>
                
            </FooterTemplate>
        </asp:Repeater>

        <asp:Repeater ID="ERepeater" runat="server">
            <HeaderTemplate>
                <div class="well-lg">
                    <span>
                        <h3>Elektrotechiek:</h3>
                    </span>
                </div>
            </HeaderTemplate>
            <ItemTemplate> 
                <div class="media balkje">                
                    <a class="pull-left" href="#">
                        <img class="media-object" src="<%# Eval("Plaatje") %>">
                    </a>
                    <div class="media-body">
                        <h4 class="media-heading"><b><%# Eval("Voornaam") + " " + Eval("Achternaam") %></b></h4>
                        <%# Eval("Beschrijving") %>
                    </div>
                </div>
            </ItemTemplate>
            <FooterTemplate>
                
            </FooterTemplate>
        </asp:Repeater>

</asp:Content>
