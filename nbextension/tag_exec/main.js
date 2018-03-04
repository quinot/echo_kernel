define([
    'base/js/namespace',
    'notebook/js/codecell'
], function (
    Jupyter,
    codecell
) {
    "use strict";

    return {
        load_ipython_extension: function () {
            console.log('[tag_execute] patching CodeCell.execute');
            var orig_execute = codecell.CodeCell.prototype.execute;
            codecell.CodeCell.prototype.execute = function (stop_on_error) {
                var root_cell = this;
                /* Lazily replace this.kernel with a proxy that will augment the
                 * message metadata with cell metadata.
                 */
                if (!this.kernel_patched) {
                    this.kernel_patched = true;

                    var this_execute = function(code, callbacks, metadata) {
                        metadata.all_cell_metadata = root_cell.metadata;
                        return root_cell.orig_kernel.execute(code, callbacks, metadata);
                    }
                    this.orig_kernel = this.kernel;
                    this.kernel = new Proxy(this.orig_kernel,
                      {"get": function(target, prop, receiver) {
                          if (prop == "execute") {
                              return this_execute;
                          } else {
                              return target[prop];
                          }
                        }
                      });
                }
                orig_execute.call(this, stop_on_error)
            };
            console.log('[tag_execute] loaded');
        }
    };
});
