/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup();
        this.title.setParts({ zopenerp: "SGEEDE ERP" }); 
    },
});
