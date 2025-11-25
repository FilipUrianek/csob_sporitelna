import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def load_excel_xls(path):
    try:
        # excely .xls potřebují xlrd==1.2.0
        return pd.read_excel(path, engine="xlrd")
    except ImportError:
        raise ImportError(
            "Pro načtení .xls souboru musíš nainstalovat xlrd 1.2.0:\n"
            "pip install xlrd==1.2.0"
        )
    except Exception as e:
        raise RuntimeError(f"Soubor {path} nejde načíst: {e}")


class BankAccount:
    def __init__(self, name, df, stats):
        self.name = name
        self.df = df
        self.stats = stats
        self.stat_vals = {}

    def compute_stats(self):
        for stat_name, col in self.stats:
            if col not in self.df.columns:
                self.stat_vals[stat_name] = {
                    "Mean": 0, "Median": 0, "Min": 0, "Max": 0
                }
                continue

            self.stat_vals[stat_name] = {
                "Mean": self.df[col].mean(),
                "Median": self.df[col].median(),
                "Min": self.df[col].min(),
                "Max": self.df[col].max()
            }

    def get_stat_vals(self):
        if not self.stat_vals:
            self.compute_stats()
        return self.stat_vals


class BankAnalysis:
    def __init__(self, accounts):
        self.accounts = accounts

    def plot_stats(self, keys):

        metrics = ["Mean", "Median", "Min", "Max"]
        rows = len(keys)
        cols = len(metrics)

        fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize=(16, 9))

        if rows == 1:
            ax = [ax]

        account_names = [acc.name for acc in self.accounts]

        for r, stat in enumerate(keys):
            for c, metric in enumerate(metrics):

                values = []
                for acc in self.accounts:
                    stats = acc.get_stat_vals()
                    values.append(stats.get(stat, {}).get(metric, 0))

                ax[r][c].bar(account_names, values, width=0.5)
                ax[r][c].set_title(f"{stat} - {metric}")
                ax[r][c].tick_params(axis='x', rotation=15)

        plt.tight_layout()
        plt.show()


def main():

    # CESTY K TVÝM SOUBORŮM
    xls_path = git push -u origin main
    csv_path = #your way to file

    # NAČTENÍ SOUBORŮ
    df_csob = load_excel_xls(xls_path)
    df_sporitelna = pd.read_csv(csv_path, delimiter=';', decimal=",")

    # DEFINICE ÚČTŮ
    csob_account = BankAccount(
        "CSOB",
        df_csob,
        [
            ("Deposit", "deposit"),
            ("Movement", "amount")
        ]
    )

    sporitelna_account = BankAccount(
        "Sporitelna",
        df_sporitelna,
        [
            ("Movement", "Castka")
        ]
    )

    analysis = BankAnalysis([csob_account, sporitelna_account])

    keys = ["Movement", "Deposit"]

    analysis.plot_stats(keys)


if __name__ == "__main__":
    main()
