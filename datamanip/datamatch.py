import pandas as pd


class DataMatcher1:
    def __init__(self, client):
        self.client = client
        pass

    def create_match_report(self, pay_df, bord_df):
        # Summarise the data
        pay_dfs = self.summarise_data(pay_df)
        bord_dfs = self.summarise_data(bord_df)

        # Change the names of each of the datasets
        pay_dfs = {k: self.change_name(v, "Pay") for k, v in pay_dfs.items()}
        bord_dfs = {k: self.change_name(v, "Bord") for k, v in bord_dfs.items()}

        # Match the datasets to each other
        match_results = self.match_datasets(pay_dfs, bord_dfs)

        # Find Remaining Data
        remaining_pay_df = self.get_remaining_data(match_results, pay_df, "Pay")
        remaining_bord_df = self.get_remaining_data(match_results, bord_df, "Bord")

        remaining_data = {"Bord_Unallocated": remaining_bord_df,
                          "Pay_Unallocated": remaining_pay_df}

        # Create 1-Key matching Report:
        match_1_key = self.create_1_key_match_report(pay_df, bord_df)

        # Create the exception reports match_1_key
        final_report = self.create_exception_reports(match_1_key, match_results)
        final_report = self.create_exception_reports(final_report, remaining_data)

        return final_report

    def summarise_data(self, df):

        df["Policy"] = df["Policy"].str.upper()
        df["Effective_Date"] = df["Effective_Date"].astype('str')

        df_group = df.groupby(['Policy', "Effective_Date"]).agg(Amount=('Amount', 'sum'),
                                                         File=('File', ', '.join)).reset_index()
        # print(df_group.head())

        df_group = df_group.groupby(['Policy'])\
            .agg(Amount=('Amount', 'sum'),
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
            "complete_match": self.strucure_bordpay_columns(complete_match),
            "check_match_1_m": self.strucure_bordpay_columns(check_match_1_m),
            "check_match_m_1": self.strucure_bordpay_columns(check_match_m_1),
            "check_match_m_m": self.strucure_bordpay_columns(check_match_m_m)
        }

        return match_results

    def match_left(self, df1, df2, key="Policy", filter_column="Bord_File"):
        # Join the data frame on the key
        joined_data = pd.merge(df1, df2, on=key, how='left')
        match = joined_data.dropna(subset=[filter_column])
        remaining = joined_data[joined_data[filter_column].isnull()]
        remaining = remaining[["Policy", "Pay_Company", "Pay_File", "Pay_Amount"]]

        return match, remaining

    def create_exception_reports(self, matching: dict, remaining: dict) -> dict:
        # for now just combine the tables
        # ToDo further analysis on the results
        return matching | remaining

    def get_remaining_data(self, matching: dict, df, pre_name: str) -> dict:
        matching_table = pd.concat(matching.values(), ignore_index=True)
        matching_table = matching_table.assign(Exclude=1)
        matching_table = matching_table.rename(columns={f'{pre_name}_Company': 'Company',
                                                        f'{pre_name}_File': 'File',
                                                        f'{pre_name}_Amount': 'Amount'})

        matching_table = matching_table[["Policy", "Company", "Exclude"]]

        # Pay Remaining - collate the matching and anti-join on the pay_df
        rem_df = pd.merge(df, matching_table, on=["Policy"], how='left')
        rem_df = rem_df[rem_df['Exclude'] != 1]
        rem_df = rem_df.drop('Exclude', axis=1)

        return rem_df

    def create_1_key_match_report(self, pay_df_raw, bord_df_raw):
        pay_df = self.summarise_1_key(pay_df_raw)
        bord_df = self.summarise_1_key(bord_df_raw)

        pay_df = self.change_name(pay_df, "Pay")
        bord_df = self.change_name(bord_df, "Bord")
        print(pay_df.head(10))
        data_matched, data_rem = self.match_1_key(pay_df, bord_df)

        # Find Remaining Data
        remaining_pay_df = self.get_remaining_data_1_key(data_matched, pay_df_raw, "Pay")
        remaining_bord_df = self.get_remaining_data_1_key(data_matched, bord_df_raw, "Bord")

        final = {"Policy Matching": self.strucure_bordpay_columns(data_matched),
                 "Bordereau Rem": self.structure_indiv_columns(remaining_bord_df),
                 "Payments Rem": self.structure_indiv_columns(remaining_pay_df)}

        return final

    def summarise_1_key(self, df):

        df["Policy"] = df["Policy"].str.upper()

        df_group = df.groupby(['Policy', 'Company']).agg(Amount=('Amount', 'sum'),
                                                         File=('File', ', '.join)).reset_index()

        df_group = df_group.groupby(['Policy']).agg(Amount=('Amount', 'sum'),
                                                    Company=('Company', ', '.join),
                                                    File=('File', ', '.join)).reset_index()

        return df_group

    def match_1_key(self, pay_df, bord_df):
        return self.match_left(pay_df, bord_df, key="Policy", filter_column="Bord_File")

    def get_remaining_data_1_key(self, matching, df, pre_name="Pay"):
        matching_table = matching.assign(Exclude=1)
        matching_table = matching_table.rename(columns={f'{pre_name}_Company': 'Company',
                                                        f'{pre_name}_File': 'File',
                                                        f'{pre_name}_Amount': 'Amount'})

        matching_table = matching_table[["Policy", "Exclude"]]


        # Pay Remaining - collate the matching and anti-join on the pay_df
        rem_df = pd.merge(df, matching_table, on=["Policy"], how='left')
        rem_df = rem_df[rem_df['Exclude'] != 1]
        rem_df = rem_df.drop('Exclude', axis=1)

        return rem_df

    def strucure_bordpay_columns(self, df):

        df = df[["Policy", "Pay_Company", "Bord_Company", "Pay_File", "Bord_File", "Pay_Amount", "Bord_Amount"]]
        df = df.assign(Difference=df['Bord_Amount'] - df['Pay_Amount'])

        return df

    def structure_indiv_columns(self, df, pre_name=""):
        if pre_name != "":
            pre_name = pre_name + "_"

        return df[["Policy", f"{pre_name}Company", f"{pre_name}File", f"{pre_name}Amount"]]


# ToDo Refactor the remaining script


class DataMatcher:
    def __init__(self, client):
        self.client = client
        pass

    def create_match_report(self, pay_df, bord_df):

        # Remove Exceptions in the Bordereau
        bord_df, bord_issues = self.remove_exceptions(bord_df, df_type="BORD")

        # Remove Exceptions in the Payments
        # pay_df, pay_issues = self.remove_exceptions(pay_df, df_type="PAY")

        # Summarise the data
        pay_df_sum = self.summarise_data(pay_df)

        # # Change the names of each of the datasets
        pay_df_sum = self.change_name(pay_df_sum, "Pay")
        bord_df = self.change_name(bord_df, "Bord")
        match, remaining_pay = self.match_left(pay_df_sum, bord_df, ["Policy", "Effective_Date"])
        remaining_bord = self.get_remaining_bord(match, bord_df, "Bord")

        final_data = {
            "Complete Matching": self.format_match(match),
            "Pay Remaining": remaining_pay,
            "Bord Remaining": remaining_bord,
            "Bordereau Duplicates": bord_issues
        }

        return final_data

    def remove_exceptions(self, df, df_type):

        # Remove instances where the date is incorrect
        issues_df = df
        remaining_df = df

        # Remove instances where there are multiple Bordereaus
        if df_type == "BORD":
            df_group = df.groupby(['Policy', 'Effective_Date']).agg(Count=('File', 'count')).reset_index()
            issues_df = df_group.query("Count != 1")
            issues_df = issues_df.drop('Count', axis=1)
            issues_df = pd.merge(issues_df, df, on=['Policy', 'Effective_Date'], how='left')
            remaining_df = df_group.query("Count == 1")
            remaining_df = remaining_df.drop('Count', axis=1)
            remaining_df = pd.merge(remaining_df, df, on=['Policy', 'Effective_Date'], how='left')
            return remaining_df, issues_df

        return remaining_df, issues_df

    def summarise_data(self, df):

        df["Policy"] = df["Policy"].astype('str')
        df["Effective_Date"] = df["Effective_Date"].astype('str')
        df["File"] = df["File"].astype('str')
        df["Company"] = df["Company"].astype('str')

        # Summarise the Payments df:
        df_group = df.groupby(['Policy', 'Effective_Date']).agg(File=('File', ', '.join),
                                                                Company=('Company', ', '.join),
                                                                Net_Amount=('Net_Amount', 'sum'),
                                                                Gross_Amount=('Gross_Amount', 'sum'),
                                                                Commission_Amount=('Commission_Amount', 'sum')
                                                                ).reset_index()

        return df_group

    def change_name(self, df, name: str):
        df = df.rename(columns={'Company': f'{name}_Company',
                                'File': f'{name}_File',
                                'Commission_Amount': f'{name}_Commission_Amount',
                                'Gross_Amount': f'{name}_Gross_Amount',
                                'Net_Amount': f'{name}_Net_Amount'})

        return df

    def match_left(self, df1, df2, keys, filter_column="Bord_File"):

        # Join the data frame on the key
        joined_data = pd.merge(df1, df2, on=keys, how='left')
        match = joined_data.dropna(subset=[filter_column])
        remaining = joined_data[joined_data[filter_column].isnull()]
        remaining = remaining[["Policy", "Effective_Date",
                               "Pay_Company", "Pay_File",
                               "Pay_Gross_Amount", "Pay_Commission_Amount", "Pay_Net_Amount"]]

        return match, remaining

    def format_match(self, df):

        df["NA_Diff"] = df["Bord_Net_Amount"] - df["Pay_Net_Amount"]
        df["GA_Diff"] = df["Bord_Gross_Amount"] - df["Pay_Gross_Amount"]
        df["CA_Diff"] = df["Bord_Commission_Amount"] - df["Pay_Commission_Amount"]
        df = df[["Policy", "Effective_Date", "Pay_Company", "Bord_Company", "Pay_File", "Bord_File",
                 "Bord_Net_Amount", "Pay_Net_Amount", "NA_Diff",
                 "Bord_Gross_Amount", "Pay_Gross_Amount", "GA_Diff",
                 "Bord_Commission_Amount", "Pay_Commission_Amount", "CA_Diff"
                 ]]

        return df

    def get_remaining_bord(self, matching, df, pre_name="Bord"):
        matching_table = matching.assign(Exclude=1)
        matching_table = matching_table[["Policy", "Effective_Date", "Exclude"]]

        # Pay Remaining - collate the matching and anti-join on the pay_df
        rem_df = pd.merge(df, matching_table, on=["Policy", "Effective_Date"], how='left')
        rem_df = rem_df[rem_df['Exclude'] != 1]
        rem_df = rem_df.drop('Exclude', axis=1)

        return rem_df
