/** @odoo-module **/
import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { FormView } from "./formView";

export class ListViewAction extends Component {
    static template = "AppOne.ListView";
    static components = { FormView };

    setup() {
        this.state = useState({
            records: [],
        });

        this.loadRecords();
        this.interval = setInterval(() => this.loadRecords(), 3000);
        onWillUnmount(() => clearInterval(this.interval));
    }

    async loadRecords() {
        const result = await rpc("/web/dataset/call_kw", {
            model: "property",
            method: "search_read",
            args: [[], ["id", "name", "postcode", "date_availability"]],
            kwargs: {},
        });
        this.state.records = result;
    }

    async createRecords() {
        await rpc("/web/dataset/call_kw", {
            model: "property",
            method: "create",
            args: [[{
                name: "new property",
                postcode: "dddh222",
                date_availability: "2025-04-04",
            }]],
            kwargs: {},
        });
        this.loadRecords();
    }

    async deleteRecord(recordId) {
        await rpc("/web/dataset/call_kw", {
            model: "property",
            method: "unlink",
            args: [[recordId]],
            kwargs: {},
        });
        this.loadRecords();
    }

    toggleCreateForm() {
        this.state.showCreateForm = !this.state.showCreateForm;
    }
    onRecordCreated(){
        this.loadRecords();
        this.state.showCreateForm = false;

    }
}


registry.category("actions").add("AppOne.action_list_view", ListViewAction);
