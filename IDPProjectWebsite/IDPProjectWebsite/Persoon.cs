using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace IDPProjectWebsite
{
    public class Persoon
    {
        public string Voornaam { get; private set; }
        public string Achternaam { get; private set; }
        public string Beschrijving { get; private set; }
        public string Plaatje { get; private set; }
        
        public Persoon(string voornaam, string Achternaam, string Beschrijving, string Plaatje)
        {
            this.Voornaam = voornaam;
            this.Achternaam = Achternaam;
            this.Beschrijving = Beschrijving;
            this.Plaatje = Plaatje;

        }
    }
}