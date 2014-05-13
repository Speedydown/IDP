using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace IDPProjectWebsite
{
    public partial class Default : System.Web.UI.MasterPage
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            MenuDiv.Visible = true;

            WebsiteMenuItem[] menuitems = {
                                            new WebsiteMenuItem("/Default.aspx", "Thuisbasis", false),
                                            new WebsiteMenuItem("/WeZijnWe.aspx", "Manage persons", false),
                                            new WebsiteMenuItem("/WatDoenWe.aspx", "Manage TV shows", false),
                                            new WebsiteMenuItem("/Contact.aspx", "Manage stats", false),
                                       };

            string url = Request.RawUrl.ToLower();

            int startindex = 0;


            int endindex = url.IndexOf(".aspx");
            string page = "";

            try
            {
                page = url.Substring(startindex, endindex - startindex + 5);
            }
            catch (Exception)
            {
                menuitems[0].Active = true;
            }

            foreach (WebsiteMenuItem w in menuitems)
            {
                if (w.ItemAdress.ToLower() == page.ToLower())
                {
                    w.Active = true;
                }
            }


            MenuRepeater.DataSource = menuitems;
            MenuRepeater.DataBind();
        }
    }


}

class WebsiteMenuItem
{
    public string ItemAdress { get; private set; }
    public string ItemName { get; private set; }
    public bool Active { get; set; }

    public WebsiteMenuItem(string ItemAdress, string ItemName, bool Active)
    {
        this.ItemAdress = ItemAdress;
        this.ItemName = ItemName;
        this.Active = Active;
    }

}