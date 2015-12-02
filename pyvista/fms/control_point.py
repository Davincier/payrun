__author__ = 'Joe'

from pyvista.rpc import DdrLister, RpcException


def get_fms_line_items(cxn, cp_nbr, fy, qtr, current_balances):
    vista_data = __get_vista_data(cxn, cp_nbr, fy, qtr)
    return __load(vista_data, current_balances)


def __get_vista_data(cxn, cp_nbr, fy, qtr):
    query = DdrLister()
    query.file = '410'
    query.fields = '.01;1;3;22;23;24;25;25.5;27;451'
    query.index = 'RB'
    query.frum = '{}-{}-{}-'.format(get_fiscal_start_date(fy, qtr), primary_source_id(cxn.source_id), cp_nbr)
    query.part = query.frum
    query.identifier = ''.join(
        [
            'S X=$S($P(^(4),U,10)]"":"Y",1:"N") ',
            'S Y=$S($P(^(7),U,6)]"":"Y",1:"N") ',
            'S Z=$P(^(0),"-")_"-"_$P(^(4),U,5) ',
            'S Z=$O(^PRC(442,"B",Z,0)) ',
            'S Z1=$S(+Z=0:"X",$P($G(^PRC(442,Z,0)),U,2)=25:$P(^(7),U,2),1:"N") ',
            'S Z2=$S(+Z\'=0:$P($$FP^PRCH0A(Z),U,2),1:"X")',
            'D EN^DDIOL(X_U_Y_U_Z1_U_Z2)'
        ]
    )
    return query.find(cxn)


FIELD_NAMES = [
    'ien',
    'txn_nbr',
    'txn_type',
    'form_type',
    'obl_amt',
    'obl_date',
    'obl_nbr',
    'adj_amt',
    'adj_cp_bal_only',
    'txn_amt',
    'purch_card_rec',
    'has_obl_validation_code',
    'had_validation_code',
    'supply_status_order',
    'obl_amt_2',
    ]


def __load(vista_data, current_balances):
    line_items = []
    for vista_line_item in vista_data:
        vista_line_item = vista_line_item[0:10] + vista_line_item[11:]
        line_item = dict(list(zip(FIELD_NAMES, vista_line_item)))

        # Get rid of the lines with no meaningful content
        if __skip(line_item):
            continue

        # Handle empty amts
        if line_item['obl_amt'] == ' ':
            line_item['obl_amt'] = None
        if line_item['txn_amt'] == ' ':
            line_item['txn_amt'] = None

        # Handle the Vista obl_date
        line_item['obl_date'] = to_py_date(line_item['obl_date'])

        # Calculate the balances
        line_item['cp_bal'] = ''
        line_item['unobl_bal'] = ''
        __set_balances(line_item, current_balances)

        # Set the statuses
        __set_statuses(line_item)

        # Handle the weird OBLs with obl_amts in last field
        if len(vista_line_item) >= 15:
            if len(line_item['obl_amt_2']) != 0 and line_item['obl_amt_2'] != 'X':
                line_item['obl_amt'] = line_item['obl_amt_2']

        # Convert the txn_nbr into fyqseq, etc.
        __replace_txn_nbr(line_item)

        # Get rid of the extra fields we needed to calc the balances and statuses
        __skim(line_item)

        line_items.append(line_item)
    return line_items


def __set_balances(line_item, current_balances):
    # Need this dict b/c we need floats, not strings
    balances = {
        'cp_bal': current_balances[0],
        'unobl_bal': current_balances[1]
    }
    txn_amt = str_to_float(line_item['txn_amt'])
    obl_amt = str_to_float(line_item['obl_amt'])

    if line_item['txn_type'] == 'C':
        balances['cp_bal'] = current_balances[0] + txn_amt
        balances['unobl_bal'] = current_balances[1] + obl_amt
    elif line_item['txn_type'] == 'A':
        balances['cp_bal'] = current_balances[0] - txn_amt
        if line_item['adj_cp_bal_only'] != 'Y':
            balances['unobl_bal'] = current_balances[1] - obl_amt
    elif line_item['txn_type'] == 'O':
        balances['cp_bal'] = current_balances[0] - txn_amt
        balances['unobl_bal'] = current_balances[1] - obl_amt
    elif line_item['txn_type'] == 'CA':
        pass
    else:
        raise RpcException('Invalid transaction type: ' + line_item['txn_type'])
    #
    # line_item['cp_bal'] = "%.2f" % balances['cp_bal']
    # line_item['unobl_bal'] = "%.2f" % balances['unobl_bal']


    line_item['cp_bal'] = balances['cp_bal']
    line_item['unobl_bal'] = balances['unobl_bal']

    current_balances[0] = round(balances['cp_bal'], 2)
    current_balances[1] = round(balances['unobl_bal'], 2)


def __set_statuses(line_item):
    if line_item['txn_type'] == 'CA':
        line_item['txn_amt_status'] = line_item['obl_amt_status'] = '#'
        return
    line_item['txn_amt_status'] = line_item['obl_amt_status'] = ''
    if len(line_item['obl_nbr']) == 0 or \
                    len(line_item['purch_card_rec']) == 0 or \
                    line_item['supply_status_order'] == 'N':
        return
    if line_item['txn_type'] == 'A':
        line_item['txn_amt_status'] = '@'
    if line_item['supply_status_order'] in ['40', '41']:
        line_item['txn_amt_status'] = line_item['obl_amt_status'] = ''
    if line_item['supply_status_order'] in ['50', '51']:
        line_item['txn_amt_status'] = '&'
    line_item['obl_amt_status'] = 'R'


def __replace_txn_nbr(line_item):
    flds = line_item['txn_nbr'].split('-')
    line_item['fy'] = flds[1]
    line_item['qtr'] = flds[2]
    line_item['cp_nbr'] = flds[3]
    line_item['seq_nbr'] = flds[4]
    line_item['fyqseq'] = ''.join([flds[1], flds[2], flds[4]])


SKIM_FIELDS = [
    'txn_nbr',
    'form_type',
    'adj_amt',
    'adj_cp_bal_only',
    'purch_card_rec',
    'has_obl_validation_code',
    'had_validation_code',
    'supply_status_order',
    'obl_amt_2',
    ]


def __skim(line_item):
    for fldname in SKIM_FIELDS:
        if fldname in line_item:
            del line_item[fldname]


def __skip(line_item):
    if line_item['txn_type'] in ['C', 'A', 'O'] and \
            (line_item['txn_amt'] == '0' or line_item['txn_amt'].strip() == '') and \
            (line_item['obl_amt'] == '0' or line_item['obl_amt'].strip() == ''):
        return True
    return False
