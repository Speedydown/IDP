using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace IDPProjectWebsite
{
    public partial class WeZijnWe : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            List<Persoon> InformaticaPersonen = new List<Persoon>();
            InformaticaPersonen.Add(new Persoon("Niels", "Riemersma", "riem1203@student.nhl.nl <br/>Projectleider", "/Images/28484_1372048216414_1088013647_30974926_3824999_n_400x400.jpg"));
            InformaticaPersonen.Add(new Persoon("Teake", "Otter", "otte0901@student.nhl.nl <br/>Aanspreekpunt I", "/Images/teeak2.0.jpg"));
            InformaticaPersonen.Add(new Persoon("Matthé", "Jacobs", "jaco1101@student.nhl.nl", "/Images/293693_190070444401510_2123158820_n.jpg"));
            InformaticaPersonen.Add(new Persoon("Miriam", "Haye", "haij1202@student.nhl.nl", "/Images/miriam.jpg"));
            InformaticaPersonen.Add(new Persoon("Ivar", "de Lange", "lang1001@student.nhl.nl", "/Images/1186113_572430379485972_171116281_n.jpg"));
            InformaticaRepeater.DataSource = InformaticaPersonen;
            InformaticaRepeater.DataBind();

            List<Persoon> WTBPersonen = new List<Persoon>();
            WTBPersonen.Add(new Persoon("Dennis", "van der Wal", "wal1102@student.nhl.nl <br/>Aanspreekpunt W", "/Images/denns.jpg"));
            WTBPersonen.Add(new Persoon("Kees", "Kempenaar", "kemp1200@student.nhl.nl", "/Images/kees.jpg"));
            WTBPersonen.Add(new Persoon("Jasper", "Talsma", "tals1302@student.nhl.nl", "/Images/jasper.jpg"));
            WTBRepeater.DataSource = WTBPersonen;
            WTBRepeater.DataBind();

            List<Persoon> EPersonen = new List<Persoon>();
            EPersonen.Add(new Persoon("Jochem", "Ludema", "lude1100@student.nhl.nl <br/>Aanspreekpunt E", "/Images/418382_270519999722978_505425335_n.jpg"));
            EPersonen.Add(new Persoon("Andre", "Poortman", "poor1100@student.nhl.nl", "/Images/andre.jpg"));
            ERepeater.DataSource = EPersonen;
            ERepeater.DataBind();
        }
    }
}