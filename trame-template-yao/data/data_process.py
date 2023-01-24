import anndata as ad
import dynamo as dyn

adata = ad.read_h5ad("./drosophila-E7-9h-models/E7-9h_cellbin_tdr_v2.h5ad")

X_counts = adata.layers["counts_X"].copy()
adata.X = adata.layers["counts_X"].copy()
dyn.pp.normalize_cell_expr_by_size_factors(adata=adata, layers="X", skip_log=False)
X_log1p = adata.X.copy()

spatial_coords = adata.obsm["3d_align_spatial"]
del adata.uns, adata.layers, adata.obsm
adata.obs = adata.obs[
    ["area", "slices", "anno_cell_type", "anno_tissue", "anno_germ_layer"]
]
adata.obsm["spatial"] = spatial_coords
adata.X = X_counts
adata.layers["X_counts"] = X_counts
adata.layers["X_log1p"] = X_log1p
print(adata)

adata.write_h5ad("./drosophila-E7-9h-models/E7-9h_cellbin.h5ad", compression="gzip")
