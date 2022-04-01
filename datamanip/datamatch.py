import pandas as pd


class DataMatcher:
    def __init__(self):
        self.match = "Yes"
        return

    def create_match_report(self, pay_df, bord_df):
        # Summarise the data
        pay_dfs = self.summarise_data(pay_df)
        bord_dfs = self.summarise_data(bord_df)

        # Change the names of each of the datasets
        pay_dfs = {k: self.change_name(v, "Pay") for k, v in pay_dfs.items()}
        bord_dfs = {k: self.change_name(v, "Bord") for k, v in bord_dfs.items()}

        print(pay_dfs["one"].head(10))

        # Match the datasets to each other
        match_results = self.match_datasets(pay_dfs, bord_dfs)

        # Find Remaining Data
        remaining_data = self.get_remaining_data(match_results, pay_df, bord_df)

        # Create the exception reports
        exception_report = self.create_exception_reports(match_results, remaining_data)

        return exception_report

    def summarise_data(self, df):
        df_group = df.groupby(['Policy', "Company"]).agg(Amount=('Amount', 'sum'),
                                                         File=('File', ', '.join)).reset_index()

        df_group = df_group.groupby(['Policy']).agg(Amount=('Amount', 'sum'),
                                                    Company=('Company', ', '.join),
                                                    Count=('Company', 'count'),
                                                    File=('File', ', '.join)).reset_index()

        df_group_1 = df_group.query("Count == 1").drop(['Count'], axis=1)
        df_group_many = df_group.query("Count != 1").drop(['Count'], axis=1)

        summarised_data = {"one": df_group_1,
                           "many": df_group_many}

        return summarised_data

    def change_name(self, df, name: str):
        df = df.rename(columns={'Company': f'{name}_Company',
                                'File': f'{name}_File',
                                'Amount': f'{name}_Amount'})

        return df

    def match_datasets(self, pay_dfs, bord_dfs):
        # match the datasets on the key first then on the Second

        # One- matches
        complete_match, remaining = self.match_left(pay_dfs["one"], bord_dfs["one"])
        check_match_1_m, remaining = self.match_left(remaining, bord_dfs["many"])

        # many- matches
        check_match_m_1, remaining = self.match_left(pay_dfs["many"], bord_dfs["one"])
        check_match_m_m, remaining = self.match_left(remaining, bord_dfs["many"])

        match_results = {
            "complete_match": complete_match,
            "check_match_1_m": check_match_1_m,
            "check_match_m_1": check_match_m_1,
            "check_match_m_m": check_match_m_m
        }

        return match_results

    def match_left(self, df1, df2, key="Policy", filter_column="Bord_File"):
        # Join the data frame on the key
        joined_data = pd.merge(df1, df2, on=key, how='left')
        match = joined_data.dropna(subset=[key])
        remaining = joined_data[joined_data[filter_column].isnull()]
        remaining = remaining[["Policy", "Pay_Company", "Pay_File", "Pay_Amount"]]

        return match, remaining

    def create_exception_reports(self, matching: dict, remaining: dict) -> dict:
        # for now just combine the tables
        # ToDo further analysis on the results
        return matching | remaining

    def get_remaining_data(self, matching: dict, pay_df, bord_df) -> dict:
        matching_table = pd.concat(matching.values(), ignore_index=True)
        matching_table = matching_table.assign(Exclude=1)
        matching_table = matching_table.rename(columns={'Pay_Company': 'Company',
                                                        'Pay_File': 'File',
                                                        'Pay_Amount': 'Amount'})

        matching_table = matching_table[["Policy", "Company", "File", "Amount", "Exclude"]]

        # Pay Remaining - collate the matching and anti-join on the pay_df
        pdl = pd.merge(pay_df, matching_table,
                       on=["Policy", "Company", "File", "Amount"], how='left')
        pdl = pdl[pdl['Exclude'] != 1]
        pdl = pdl.drop('Exclude', axis=1)

        # Bord Remaining - collate the matching and anti-join on the bord_df
        matching_table = pd.concat(matching.values(), ignore_index=True)
        matching_table = matching_table.assign(Exclude=1)
        matching_table = matching_table.rename(columns={'Bord_Company': 'Company',
                                                        'Bord_File': 'File',
                                                        'Bord_Amount': 'Amount'})

        matching_table = matching_table[["Policy", "Company", "File", "Amount", "Exclude"]]

        bdl = pd.merge(bord_df, matching_table,
                       on=["Policy", "Company", "File", "Amount"], how='left')
        bdl = bdl[bdl['Exclude'] != 1]
        bdl = bdl.drop('Exclude', axis=1)

        remaining = {"Bord_Unallocated": bdl,
                     "Pay_Unallocated": pdl
                     }

        return remaining

# ToDo Refactor the remaining script
