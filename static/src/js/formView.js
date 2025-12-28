/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class FormView extends Component {
    static template = "AppOne.FormView";

    setup() {
        this.state = useState({ name: "", postcode: "", date_availability: "" });
    }

    async createRecord() {
        await rpc("/web/dataset/call_kw", {
            model: "property",
            method: "create",
            args: [[{
                name: this.state.name,
                postcode: this.state.postcode,
                date_availability: this.state.date_availability,
            }]],
            kwargs: {},
        });
        this.props.onRecordCreated();
    }

    cancel() {
        this.state.name = "";
        this.state.postcode = "";
        this.state.date_availability = "";
        this.props.onCancel()
    }
}
