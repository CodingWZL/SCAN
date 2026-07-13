# SCAN Web

The new SCAN interface is a static React application designed for GitHub Pages. It preserves the full formulation controls from the Streamlit app and moves inference into the browser through ONNX Runtime Web. Atlas search uses DuckDB-Wasm to query the three published Parquet partitions without a Python server.

## Local development

```bash
pnpm install
pnpm dev
```

Run `python tools/export_web_assets.py` from the repository root whenever the PyTorch checkpoint or descriptor tables in `app/web.py` change.

## Deployment and domain

Merging to `main` deploys `web/dist` through GitHub Pages. The default project URL is `https://codingwzl.github.io/SCAN/`. A domain such as `electrolyte.io` must be registered separately, then added as the custom domain in the repository Pages settings with the required DNS records.

## Analytics

The Analytics page intentionally ships without fingerprinting or a hard-coded vendor token. Set `VITE_ANALYTICS_ENDPOINT` in the build environment when a privacy-friendly analytics backend is selected. The UI is designed to accept totals and city/country coordinates from Plausible, Umami, or a small Cloudflare Worker adapter.
