/*@odoo-module */
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

const actionRegistry = registry.category("actions");

class DashboardScanLabel extends Component {
    setup() {
        super.setup();
        this.barcode = "";
        this.onKeyDown = this.onKeyDown.bind(this);  // Bind the method to ensure correct context
        document.addEventListener('keydown', this.onKeyDown);
        this.count_success = 0
        this.count_failed = 0
    }

    /**
     * Method untuk menangani input barcode.
     * @param {string} barcode - Barcode yang dipindai.
     */
    handleBarcodeInput(barcode) {
        var success_box = $(".success-box")
        var failed_box = $(".failed-box")
        if (success_box.length > 0 || failed_box.length > 0){
            console.log("Barcode dipindai:", barcode);
            // Tambahkan logika pemrosesan barcode di sini
            var ajax = $.ajax({
                method: 'POST',
                url: '/my_future/send_barcode',
                data: {
                    'barcode': barcode,
                },
                dataType: 'json',
                success: function(data) {
                    console.log(data[0].name,"data")
                    console.log(data[0].count,'count')
                    if (data[0].name === 'success'){
                        
                        let matches = success_box[0].innerHTML.match(/(\d+)/);
                        let new_number = parseInt(matches) + 1
                        success_box[0].innerHTML = "Success Scan : " + new_number
                    } else {
                        let matches = failed_box[0].innerHTML.match(/(\d+)/);
                        let new_number = parseInt(matches) + 1
                        failed_box[0].innerHTML = "Failed Scan : " + new_number
                    }
                }
            })
        }
    }

    /**
     * Event listener untuk menangkap input barcode.
     * @param {KeyboardEvent} event - Event keyboard.
     */
    onKeyDown(event) {
        if (event.key === 'Enter') {
            if (this.barcode) {
                this.handleBarcodeInput(this.barcode);
                this.barcode = "";
            }
        } else {
            this.barcode += event.key;
        }
    }

    willUnmount() {
        super.willUnmount();
        document.removeEventListener('keydown', this.onKeyDown);
    }
}


DashboardScanLabel.template = "my_future_custom.DashboardScanLabel";
// Tag name yang kita masukkan di langkah pertama.
actionRegistry.add("DashboardScanLabel.tag", DashboardScanLabel);

export default DashboardScanLabel;