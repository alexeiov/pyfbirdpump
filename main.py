import cond_updater
#import xlsx_import
import config


if __name__ == '__main__':
    # wb = xlsx_import.get_xlsx_data()
    # data = xlsx_import.make_data_list_mult_col(wb)
    # cond_updater.cond_update(data, config.db_addresses['ref'])
    cond_updater.cond_update_from_db(config.db_addresses['ref']) #adds rates and other to MT and therefore works for LK, for KVA need to update to add to separate table
