from app.src.services.user import get_user_by_id
from app.src.models.models import JobRating
from datetime import datetime


def employeer_stats(employeer_id):
    employeer = get_user_by_id(employeer_id)

    statAll = []

    for offer in employeer.job:
        ratings = {
            'id': offer.id,
            'rQ': 0,
            'allR': 0,
            'd30R': 0,
            'empInfR':[]
        }
        tTime = datetime.today()
        rAllctr = 0
        r30ctr = 0

        for r  in JobRating.query.filter_by(job_id = offer.id).all():

            empInfR = {
                'pos': ", ".join([ei.position for ei in r.employee.experience]),
                'rat': r.rating
            }

            ratings['allR'] += r.rating
            rAllctr += 1
            if (tTime - r.created_at).days <= 30:
                ratings['d30R'] += r.rating
                r30ctr += 1

            ratings['empInfR'].append(
                empInfR
            )

        if rAllctr:
            ratings['allR'] /= rAllctr
            ratings['rQ'] = rAllctr
        if r30ctr:
            ratings['d30R'] /= r30ctr

        statAll.append(
            ratings
        )
    
    print(statAll)

    return statAll
