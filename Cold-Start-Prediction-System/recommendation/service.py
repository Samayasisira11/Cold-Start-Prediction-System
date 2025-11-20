from django.db.models import Sum

from recommendation.beans import ProductBean
from recommendation.models import RatingModel, CommentModel, ProductModel, TransactionModel

def getProductById(productid):

    product=ProductModel.objects.get(id=productid)
    product.path = str(product.path).split("/")[1]

    comments = CommentModel.objects.filter(product=product.id)

    rating = 0
    count = 0

    for ratingmodel in RatingModel.objects.filter(product=product.id):
        rating = rating + int(ratingmodel.rating)
        count = count + 1

    totalrating = 0

    print("rating", rating)
    print("count", count)

    try:
        totalrating = int((rating / count))
    except Exception as e:
        print(e)

    print(totalrating)

    bean = ProductBean(product, comments, totalrating, product.description)

    return bean

def getAllProducts():

    products = []

    for product in ProductModel.objects.all():

        product.path = str(product.path).split("/")[1]

        comments = CommentModel.objects.filter(product=product.id)

        rating = 0
        count=0

        for ratingmodel in RatingModel.objects.filter(product=product.id):
            rating=rating+int(ratingmodel.rating)
            count=count+1

        totalrating=0

        print("rating",rating)
        print("count", count)

        try:
            totalrating=int((rating / count))
        except Exception as e:
            print(e)

        print(totalrating)

        bean = ProductBean(product, comments,totalrating,product.description)

        products.append(bean)

    return products


def findrecommendations(userid):

    products=set()

    frequencymap=dict()

    myrasactions=TransactionModel.objects.filter(userid=userid)

    otherstrasactions = TransactionModel.objects.exclude(userid=userid)

    for mytransaction in myrasactions:

        for othertransaction in otherstrasactions:

            if mytransaction.productid in othertransaction.productid:

                myrating=0
                rmodel=RatingModel.objects.filter(user=userid,product=mytransaction.productid).first()
                if rmodel is not None:
                    myrating=rmodel.rating

                userrating=0
                rmodel =RatingModel.objects.filter(user=othertransaction.userid,product=othertransaction.productid).first()
                if rmodel is not None:
                    userrating=rmodel.rating

                productrating=RatingModel.objects.filter(product=mytransaction.productid).aggregate(Sum('rating'))

                ratingdiff=int(myrating)-int(userrating)

                if ratingdiff<=2 and ratingdiff>=-2 or userrating == 0 or myrating == 0 or productrating == 0:
                    if othertransaction.userid in frequencymap.keys():
                        frequencymap[othertransaction.userid]=frequencymap[othertransaction.userid]+1
                    else:
                        print("other:",userid)
                        frequencymap.update({othertransaction.userid:1})

    sorteddict={k: v for k, v in sorted(frequencymap.items(), key=lambda item: item[1])}

    for user in sorteddict.keys():
        transactons = TransactionModel.objects.filter(userid=user)
        for transaction in transactons:
            product=ProductModel.objects.filter(id=transaction.productid).first()
            product.path = str(product.path).split("/")[1]
            products.add(product)

    return products



