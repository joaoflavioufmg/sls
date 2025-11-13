def distribuicoes(tipo):
    return {
        # Cada segundo real, representa 60 min 
        "registro": random.gammavariate(46170.588,152.333),
        "conferencia_NF": random.gauss(80.000,20.000),
        "frac_manual": random.weibullvariate(283.546,16.000),
        "frac_auto": random.weibullvariate(35.520,-8.152),
        "dispensa": random.lognormvariate(6.979,53.635),
        "producao_fita": random.betavariate(0.733,1.191),
        
#        "XXXXX": random.gauss(35.350,2.443), #tempo da bolsa descer e a pessoa ficar de observação
        }.get(tipo,0.0)

        lognormvariate