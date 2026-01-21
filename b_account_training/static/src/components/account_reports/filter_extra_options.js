/** @odoo-module */

import { AccountReportFilterExtraOptions } from "@account_reports/components/account_report/filters/extra_options";
import { patch } from "@web/core/utils/patch";

patch(AccountReportFilterExtraOptions.prototype, {
    filterClicked(params) {
        if (params.optionKey === 'training_entries') {
            const options = { ...this.controller.options };
            options.training_entries = !options.training_entries;
            this.controller.updateSearchParams({ options });
            if (params.reload) {
                this.controller.reload();
            }
        } else {
            super.filterClicked(params);
        }
    },
});