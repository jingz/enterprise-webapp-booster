from . import *
import app.inquiries as InqModels

bp = Blueprint('inquiry_api', __name__)
before_request_extract_page_params(bp)
# before_request_extract_inquiry_params(bp)

_g = {}

# @bp.before_request
# def __extract_model():
#     model = request.args.get('model', None)
#     _g['model'] = getattr(InqModels, model, None) 
#     if _g['model']:
#         _g['condition_text'] = _g['model'].readable_search_clause(request.args)

from app.reports.sqla_exporter import gen_pdf
def __export_pdf():
    m = _g['model']
    if m:
        res = m.search(request.args)
        # res = Client.query.filter("total_credit_limit > 0").order_by("total_credit_limit desc").limit(90)
        if res.count() > 10000:
            return render_fail("Record Exceed Limit")

        pdf = gen_pdf(res, **_g)
        return send_file(pdf, mimetype='application/pdf',
            attachment_filename='test.pdf', as_attachment=True)
    else:
        return render_fail("Cannot Export PDF %s" % m)


from app.reports.sqla_exporter import gen_xl
def __export_xl():
    m = _g['model']
    if m:
        res = m.search(request.args)
        # res = Client.query.filter("total_credit_limit > 0").order_by("total_credit_limit desc").limit(90)
        if res.count() > 10000:
            return render_fail("Record Exceed Limit")

        xl = gen_xl(res, **_g)
        return send_file(xl, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                attachment_filename='xxl.xlsx', as_attachment=True)
        #  return send_file(xl, mimetype='application/vnd.ms-excel')
    else:
        return render_fail("Cannot Export Excel %s" % m)


def __handle_inq(model):
    ''' handle all incoming query for every inquiry model
    '''
    m = getattr(InqModels, model, None)
    if m:
        _g['model'] = m
        _g['condition_text'] = m.readable_search_clause(request.args)

        if request.args.get('export_pdf', None):
            return __export_pdf()
        elif request.args.get('export_xl', None):
            return __export_xl()
        else:
            c = m.search(request.args)
            return render_records(c)
    else:
        return render_fail('Invalid Request')


@bp.route('/ord_deal_inq')
def __list_ord_deal_inq():
    return __handle_inq('OrdDealInq')

