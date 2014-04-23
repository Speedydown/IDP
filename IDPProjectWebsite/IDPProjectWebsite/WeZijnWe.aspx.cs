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
            InformaticaPersonen.Add(new Persoon("Niels", "Riemersma", "iK BEN NIELS EN IK BEN EEN BEETJE RAAR", "/Images/64x64.png"));
            InformaticaPersonen.Add(new Persoon("Matthé", "Jacobs", "Ik ben Matthe, 21 jaar en woon sinds kort in leeuwarden, hier ga ik helemaal los met de wildste feestjes!", "/Images/64x64.png"));
            InformaticaPersonen.Add(new Persoon("Miriam", "Haye", "Hoi!", "/Images/64x64.png"));
            InformaticaPersonen.Add(new Persoon("Ivar", "de Lange", "XBONE!", "/Images/64x64.png"));
            InformaticaPersonen.Add(new Persoon("Teake", "Otter", "Wat is dit kut zeg!.", "/Images/64x64.png"));
            InformaticaRepeater.DataSource = InformaticaPersonen;
            InformaticaRepeater.DataBind();

            List<Persoon> WTBPersonen = new List<Persoon>();
            WTBPersonen.Add(new Persoon("Kees", "Kempenaar", "Ja", "/Images/64x64.png"));
            WTBPersonen.Add(new Persoon("Jasper", "Talsma", "WTB KAN NIKS OLE", "/Images/64x64.png"));
            WTBPersonen.Add(new Persoon("Dennis", "van der Wal", "Ja", "/Images/64x64.png"));
            WTBRepeater.DataSource = WTBPersonen;
            WTBRepeater.DataBind();

            List<Persoon> EPersonen = new List<Persoon>();
            EPersonen.Add(new Persoon("Andre", "Poortman", "Ja", "/Images/64x64.png"));
            EPersonen.Add(new Persoon("Jochem", "Ludema", "EE", "/Images/64x64.png"));
            ERepeater.DataSource = EPersonen;
            ERepeater.DataBind();
        }
    }
}