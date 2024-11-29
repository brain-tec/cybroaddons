/** @odoo-module */
import { Orderline } from "@point_of_sale/app/store/models"
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { CustomButtonPopup } from "./CustomPopup";

patch(Orderline.prototype,  {

    async set_quantity(quantity, keep_price) {
//      Checking the orderline quantity and onhand lot quantity
        super.set_quantity(quantity, keep_price);
        var lines = await this.get_lot_lines()
        var pos_config_id = this.pos.config.id
        if(lines.length){
            var product_id = this.get_product().id
            var lot_name = lines.map(line => line.lot_name).pop();

            const result = await this.pos.orm.call(
                "stock.lot", "get_available_lots_qty_pos", [product_id, lot_name, pos_config_id], {}
            )
            if (result != 0 && lines.length == 1) {
                if (quantity > result) {
                    this.quantity = result;
                    await this.env.services.popup.add(CustomButtonPopup, {
                        title: _t("Exception"),
                        body: _t("Product quantity Exceeding the allowed lot quantity")
                    });
                }
            } else if (result == 0) {
                const order = this.pos.get_order();
                const selectedLine = order.get_selected_orderline();
                selectedLine.stock = result;
                if (quantity === 1 && lines.length >= 1) {
                    order._unlinkOrderline(selectedLine);
                }
                else if (quantity >=1) {
                    const Length = selectedLine.pack_lot_lines.length
                    const LastLine = selectedLine.pack_lot_lines[Length - 1]
                    selectedLine.pack_lot_lines.remove(LastLine)
                    selectedLine.set_quantity(quantity - 1, keep_price)
                }
                this.env.services.popup.add(ErrorPopup, {
                        title: _t("No Stock Available"),
                        body: _t(
                            "The requested lot:" + lot_name + "is currently out of stock."
                        ),
                    });
            }

        }
    }
});
