
class DataMatcher:
    def __init__(self):
        self.match = "Yes"
        return

    def create_match_report(self, pay_df, bord_df):

        # Summarise the data
        pay_dfs = self.summarise_data(pay_df)
        bord_dfs = self.summarise_data(bord_df)
        print(pay_dfs)
        print(pay_dfs[0])
        # Change the names of each of the datasets
        pay_dfs = [lambda x: self.change_name(x, "Pay") for x in pay_dfs]
        # bord_df = self.change_name(bord_df, "Bord")



        # Match the datasets to each other

        # Create the exception reports

        # Create the remaining dataset

        # Save the tables in an excel summary sheet.
        return

    def summarise_data(self, df):
        df_group = df.groupby(['Policy', "Company"]).agg(Amount=('Amount', 'sum'),
                                                         File=('File', ', '.join)).reset_index()

        df_group = df_group.groupby(['Policy']).agg(Amount=('Amount', 'sum'),
                                                    Company=('Company', ', '.join),
                                                    Count=('Company', 'count'),
                                                    File=('File', ', '.join), ).reset_index()

        df_group_1 = df_group.query("Count == 1").drop(['Count'], axis=1)
        df_group_many = df_group.query("Count != 1").drop(['Count'], axis=1)

        return df_group_1, df_group_many

    def change_name(self, df, name: str):
        return df.rename(columns={'Company': f'{name}_Company',
                                  'File': f'{name}_File',
                                  'Amount': f'{name}_Amount'},
                         inplace=True)


    def match_datasets(self):
        # match the datasets on the key first then on the Second

        return

    def create_exception_reports(self):
        return

    def get_remaining_data(self):
        return

    def save_summary_tables(self):
        return
