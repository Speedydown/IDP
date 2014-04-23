<%@ Page Title="" Language="C#" MasterPageFile="~/Default.Master" AutoEventWireup="true" CodeBehind="WatDoenWe.aspx.cs" Inherits="IDPProjectWebsite.WatDoenWe" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">

    
    <div class="well-lg">
        <h2>Wat doet Tracheata:</h2>
        <h3>Projectopdracht:</h3>
        <div>
            <span>
                De drie opleidingen Informatica, Werktuigbouwkunde en Elektrotechniek slaan de handen ineen om in dit project een 6-potige smart spider te ontwikkelen. Deze spider, of spin, 
                moet aan verschillende eisen voldoen en een aantal tests doorstaan. Hiervoor wordt ook een wedstrijd georganiseerd om te kijken wat de beste spin is.
            </span>
        </div>

        <div>
            <span>
                <h3>Specificaties spin:</h3>
            </span>
            <span>
                <div class="well-lg">
                    <li>De spin heeft 6 poten met 3 vrijheidsgraden per poot. </li>
                    <li>Aan de afmetingen van de spin worden geen specifieke eisen gesteld, behalve dan dat 
                        deze aan alle wedstrijdonderdelen moet meedoen, waaronder de doorgang door een poort van gedefinieerde afmetingen. </li>
                    <li>Voor de constructie van de poten moeten servo’s worden gebruik, 3 servo’s per poot. </li>
                    <li>Alle poten hebben minimaal dezelfde functionaliteit; de voorpoten moeten daarnaast en onafhankelijk en op afstand bestuurbare (prik)functie. Zie ook specificatie 13. </li>
                    <li> De spin draagt zijn eigen voeding (accu, batterij), maar mag in de testfase uiteraard ook aan een draadje wandelen. De wedstrijdonderdelen zijn batterij gevoed. </li>
                    <li>De spin moet worden voorzien van een Raspberry Pi voor besturing, beeldherkenning en autonomie. Daarnaast mag de spin van allerlei subsystemen worden voorzien, zoals IO-modules of interfaces voor sensoren. Het is ook toegestaan bepaalde functies gedistribueerd uit te voeren, d.w.z. in combinatie met server-componenten (op afstand). </li>
                    <li>De spin moet worden voorzien van een camera voor o.a. de beeldherkenning. Daarnaast moet de spin worden voorzien van een hoek- of hellingsensor voor bepaling van de helling van de spin en moet de accuspanning kunnen worden gemeten. </li>
                    <li>De spin moet op zijn “achterlijf”, op hoogte van het aangrijpingspunt van de poten, een draagplatvorm hebben dat ruimte biedt aan een (standaard) plastic koffiebekertje. Het bekertje mag op de spin gefixeerd worden. </li>
                    <li>Het basisgedrag van de spin moet op afstand bestuurd kunnen worden via een tablet of smartphone (Android/Java; IOS/Objective-C). </li>
                    <li>Het moet mogelijk zijn het beeld van de camera op de spin te streamen.</li>
                    <li>De spin moet beeldherkenning hebben.</li>
                </div>
            </span>
        </div>
        <div>
            <span>
                <h3>Wedstrijdonderdelen:</h3>
            </span>
            <span>
                <div class="well-lg">
                    <li>Limbo-test:	De spin moet binnen 1 minuut tussen 2 poorten bewegen die bepaalde afmetingen hebben.</li>
                    <li>De spider race: Parkour van 4 meter waar alle spinnen aan meedoen. De spin die het eerste over de finish komt wint.</li>
                    <li>So you think you can dance: Er moet 2 minuten gedanst worden en de spin die het meest creatief danst wint. </li>
                    <li>De spinnijdig-race: De spin moet een hindernis baan afleggen met een bekertje water op zijn rug. De snelste spin wint. </li>
                    <li>De “Spider Gap”: De spin moet over een uit twee delen bestaand plateau met een kloof ertussen bewegen. Er kan gebruikt gemaakt worden van een smal bruggetje en een ring die er boven hangt. Hier gaat het ook om de snelste tijd.</li>
                    <li>De Zwarte weduwe op oorlogspad: In dit onderdeel is er een speelveld met drie ballonnen en de spin die ze het snelt heeft lek geprikt wint.</li>
                    <li>Spinnen in de olie: In een afgebakend gebied moet de spin 3 teerballen binnen 5 minuten lokaliseren. De snelste tijd wint.</li>
                    <li>De paringsdans (bonusonderdeel): Alle spinnen staan in een cirkel om een ballon en de spin die als eerst de ballon lek prikt wint.</li>
                </div>
            </span>

        </div>
        <div>
            <span>
                <h3>Beeld:</h3>
            </span>
            <span>
                <div class="well-lg">
                    <iframe width="800px" height="380px" src="//www.youtube.com/embed/fa7IAvvYPOs" frameborder="0" allowfullscreen></iframe>
                </div>
            </span>

        </div>

        


   </div>


</asp:Content>
