/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { Dialog } from "@web/core/dialog/dialog";
import { 
	odooExceptionTitleMap,
	ErrorDialog, 
	ClientErrorDialog, 
	NetworkErrorDialog, 
	WarningDialog, 
	RedirectWarningDialog, 
	RPCErrorDialog,
	SessionExpiredDialog
} from "@web/core/errors/error_dialogs";

ErrorDialog.title = _lt("SGEEDE ERP Error");
ClientErrorDialog.title = _lt("SGEEDE ERP Client Error");
NetworkErrorDialog.title = _lt("SGEEDE ERP Network Error");
SessionExpiredDialog.title = _lt("SGEEDE ERP Session Expired");

patch(SessionExpiredDialog, {
    components: { ...SessionExpiredDialog.components, Dialog },
});

patch(RPCErrorDialog.prototype, {
    inferTitle() {
        if (this.props.exceptionName && odooExceptionTitleMap.has(this.props.exceptionName)) {
            this.title = odooExceptionTitleMap.get(this.props.exceptionName).toString();
            return;
        }
        if (!this.props.type) {
            return;
        }
        switch (this.props.type) {
            case "server":
                this.title = _lt("SGEEDE ERP Server Error");
                break;
            case "script":
                this.title = _lt("SGEEDE ERP Client Error");
                break;
            case "network":
                this.title = _lt("SGEEDE ERP Network Error");
                break;
        }
    }
});

patch(WarningDialog.prototype, {
    inferTitle() {
        if (this.props.exceptionName && odooExceptionTitleMap.has(this.props.exceptionName)) {
            return odooExceptionTitleMap.get(this.props.exceptionName).toString();
        }
        return this.props.title || _lt("SGEEDE ERP Warning");
    }
});

patch(RedirectWarningDialog.prototype, {
    setup() {
    	this._super(...arguments);
        this.title = capitalize(subType) || _lt("SGEEDE ERP Warning");
    }
});
