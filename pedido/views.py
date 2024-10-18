from django.db.models.fields import CommaSeparatedIntegerField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Pedido, ItemPedido, CupomDesconto, HistoricoPedido
from produto.models import Produto, Categoria
import json
def finalizar_pedido(request):  
    if request.method == "GET":
        categorias = Categoria.objects.all()
        erro = request.GET.get('erro')
        carrinho = request.session.get('carrinho', [])
        total = sum([float(i['preco']) for i in carrinho])
        return render(request, 'finalizar_pedido.html', {'carrinho': len(carrinho),
                                                        'categorias': categorias,
                                                        'total': total,
                                                        'erro': erro})
    else:
        carrinho = request.session.get('carrinho', [])
        if len(carrinho) > 0:
            x = request.POST
            total = sum([float(i['preco']) for i in carrinho])
            cupom = CupomDesconto.objects.filter(codigo=x.get('cupom')).first()
            cupom_salvar = None

            if cupom and cupom.ativo:
                total = total - ((total * cupom.desconto) / 100)
                cupom.usos += 1
                cupom.save()
                cupom_salvar = cupom

            listaCarrinho = []
            for i in carrinho:
                produto = Produto.objects.filter(id=i['id_produto']).first()
                if produto:
                    listaCarrinho.append({
                        'produto': produto,
                        'observacoes': i.get('observacoes', ''),
                        'preco': i['preco'],
                        'adicionais': i.get('adicionais', ''),
                        'quantidade': i['quantidade'],
                    })

            troco_para = x.get('troco_para', '')
            lambda_func_troco = lambda: int(troco_para) - total if troco_para else ""
            lambda_func_pagamento = lambda: 'Cartão' if x.get('meio_pagamento') == '2' else 'Dinheiro'

            pedido = Pedido(
                usuario=x.get('nome', ''),
                total=total,
                troco=lambda_func_troco(),
                cupom=cupom_salvar,
                pagamento=lambda_func_pagamento(),
                ponto_referencia=x.get('pt_referencia', ''),
                cep=x.get('cep', ''),
                rua=x.get('rua', ''),
                numero=x.get('numero', ''),
                bairro=x.get('bairro', ''),
                telefone=x.get('telefone', ''),
            )
            pedido.save()

            ItemPedido.objects.bulk_create(
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto'],
                    quantidade=v['quantidade'],
                    preco=v['preco'],
                    adicionais=str(v['adicionais'])
                ) for v in listaCarrinho
            )

            request.session['carrinho'] = []  # Limpar o carrinho corretamente
            request.session.save()

            return render(request, 'pedido_realizado.html')
        else:
            return redirect('/pedidos/finalizar_pedido?erro=1')


def validaCupom(request):
    cupom = request.POST.get('cupom')
    cupom = CupomDesconto.objects.filter(codigo=cupom)
    if len(cupom) > 0 and cupom[0].ativo:
        desconto = cupom[0].desconto
        total = sum([float(i['preco']) for i in request.session['carrinho']])
        total_com_desconto = total - ((total * desconto) / 100)
        data_json = json.dumps({
            'status': 0,
            'desconto': desconto,
            'total_com_desconto': str(total_com_desconto).replace('.', ',')
        })
        return HttpResponse(data_json)
    else:
        return HttpResponse(json.dumps({'status': 1}))
