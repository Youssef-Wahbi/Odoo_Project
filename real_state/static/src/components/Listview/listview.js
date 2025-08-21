/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.state = useState({ properties: [] });

        onWillStart(async () => {
            await this.loadRecords();
            this.interval = setInterval(() => this.loadRecords(), 3000);
        });

        onWillUnmount(() => {
            if (this.interval) clearInterval(this.interval);
        });
    }

    // async loadRecords() {
    //     const records = await this.orm.searchRead("property", [], []);
    //     this.state.properties = records;
    // }

    async loadRecords() {
        const records = await this.rpc("/web/dataset/call_kw", {
            model: "property",
            method: "search_read",
            args: [],
            kwargs: {
                fields: ["name", "expected_price", "state", "bedrooms"],
                domain: [],
                limit: 100
            }
        });
        this.state.properties = records;
    }

    async createRecord() {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "property",
            res_id: false,
            view_mode: "form",
            target: "new",
            views: [[false, "form"]],
            context: {
                default_name: "New Property",
                default_expected_price: 0,
                default_bedrooms: 2,
                default_state: "draft"
            }
        });
    }

    async deleteRecord(ev) {
        const recordId = ev.target.getAttribute('data-id');
        if (recordId && confirm('Are you sure you want to delete this property?')) {
            try {
                await this.rpc("/web/dataset/call_kw", {
                    model: "property",
                    method: "unlink",
                    args: [[parseInt(recordId)]],
                    kwargs: {}
                });
                // Refresh the list after deletion
                await this.loadRecords();
            } catch (error) {
                console.error("Error deleting property:", error);
            }
        }
    }
}

ListViewAction.template = "ListViewAction";
ListViewAction.props = {
    action: Object,
    actionId: Number,
    className: String,
};

registry.category("actions").add("real_state.listview_action", ListViewAction);
