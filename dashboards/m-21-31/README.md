# M-21-31 Documentation

## 1. To Deploy

Deploying M-21-31 is simple. Follow these steps:

1. Take the dashboard configuration file `m-21-31.conf` and paste it into the account.

<img width="1893" alt="image" src="https://github.com/user-attachments/assets/90feb949-fa97-4469-a26a-ccc66dd330a9" />


2. Export the following Google Spreadsheet as a CSV file:
   - [M-21-31 Mapping Sheet](https://docs.google.com/spreadsheets/d/120NWtQXE-DAgBftd-h6weXnqPqdLBy_reTTNcdMusOE/edit?pli=1&gid=1925210520#gid=1925210520)
3. Save the exported file as `m2131.csv` and save it to `/datatables/m2131.csv`
4. Add the following stanza to the alerts (watchlist JSON):
   - [M-21-31 Alerts File](https://docs.google.com/document/d/1TD2jRa5ypT0yfoTrqS82rXijDS7hPHasF7gO4emIf1Q/edit?tab=t.0)

Once these steps are completed, you will have:
- A functional dashboard
- A lookup table (`m2131.csv`) for mappings
- An alerts file that checks every minute if alerts match the defined mappings

---

## 2. Adding Detections

To add detections:

1. Open the `alerts.json` file.
2. Add more `query-m21` queries to the alerts file.
3. Map each `query-m21` to a corresponding requirement in the `m2131.csv` file.

### Example:
If the `m2131.csv` file contains the following:
```csv
1,Identity & Credential Management,Account Creation,0
```

Then in `alerts.json`, you will map it as:
```json
{
  "requirement": "1",
  "query-m21": "type_uid = 300101"
}
```

Each new detection should follow the same structure, ensuring that queries align with requirement IDs.

---

## 3. Managing Mappings

Mappings between requirements and queries are handled via the `m2131.csv` file and the `alerts.json` file:

- The **primary key** in `m2131.csv` is the **requirement ID**.
- In `alerts.json`, each query is mapped to a requirement using the requirement ID.
- Queries in `alerts.json` should reference the correct requirement ID from `m2131.csv`.

### Example Mapping:
#### `m2131.csv`:
```csv
1,Identity & Credential Management,Account Creation,0
```
#### `alerts.json`:
```json
{
  "requirement": "1",
  "query-m21": "type_uid = 300101"
}
```

### Managing Mappings Effectively:
1. Ensure each requirement ID in `m2131.csv` corresponds to an entry in `alerts.json`.
2. Update `alerts.json` whenever a new detection rule is added.
3. Regularly validate the mappings to ensure they are still relevant.

By following this structure, M-21-31 remains organized and easy to maintain.
