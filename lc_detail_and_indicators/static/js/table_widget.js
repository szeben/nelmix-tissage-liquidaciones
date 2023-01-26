odoo.define(
    'web.TableMetricsWidget',
    ['web.core', 'web.AbstractField', 'web.field_registry'],
    function (require) {
        "use strict";

        const QWeb = require('web.core').qweb;
        const AbstractField = require('web.AbstractField');
        const fieldRegistry = require('web.field_registry');

        const TableMetricsWidget = AbstractField.extend({
            xmlDependencies: ['/lc_detail_and_indicators/static/xml/table_template.xml'],
            _renderReadonly: function () {
                this.$el.html(QWeb.render('lc_detail_and_indicators.table_metrics', {
                    lines: JSON.parse(this.value),
                }));
            },
        });

        fieldRegistry.add('table_metrics', TableMetricsWidget);
        return TableMetricsWidget;
    }
);