

def prepare_silica_nanoparticles(P20, P300, stock_vials, sample_well, ethanol_vol, ammonia_vol, water_vol, TEOS_vol):
    """
    OT2 procedure to prepare silica nanoparticle samples

    Parameters:
    -----------
    P20: OT2 P20 pipette object
    P300: OT2 P300 pipette object
    stock_vials: dictionary of {'solution name':Well} pairs  for stock vials. Names should be 'ethanol', 'ammonia', 'water', 'TEOS'
    sample_well: well to prepare sample in
    ethanol_vol: Volume of ethanol to add (float, uL)
    ammonia_vol: Volume of ammonia to add (float, uL)
    water_vol: Volume of water to add (float, uL)
    TEOS_vol: Volume of TEOS to add (float, uL)


    Return:
    ------
    none
    """

    ethanol_stock = stock_vials['ethanol']
    ammonia_stock = stock_vials['ammonia']
    water_stock = stock_vials['water']
    TEOS_stock = stock_vials['TEOS']

    # Decide which pipette to use for each transfer:

    ethanol_transfers = decide_pipette(ethanol_vol)
    ammonia_transfer = decide_pipette(ammonia_vol)
    water_transfer = decide_pipette(water_vol)
    TEOS_transfer = decide_pipette(TEOS_vol)
    # add water and TEOS 




    # execute ethanol transfers
    execute_transfer(ethanol_transfers, ethanol_stock, sample_well)
    execute_transfer(ammonia_transfer, ammonia_stock, sample_well)
    execute_transfer(water_transfer, water_stock, sample_well, mix = (15, 300))
    execute_transfer(TEOS_transfer, TEOS_stock, sample_well, mix = (15, 300))

    return

def decide_pipette(P20, P300, volume):
    """
    Given a volume, decide if a P20 or P300 pipette should be used to transfer

    return: 'P20' or 'P300'
    """

    assert volume < 400, 'Volume must be less than 400 uL'

    if volume < 20:
        transfer = [{'pipette':P20, 'vol':volume}]
    
    elif volume > 20:
        # more complex logic to decide how to divide transfers 
        if volume < 300:
            transfer = [{'pipette':P300, 'vol':volume}]
        if volume > 300:
            transfer_vol = volume/2
            transfer = [{'pipette':P300, 'vol':transfer_vol}]*2

    
    return transfer

def execute_transfer(transfer_dict, source_well, sample_well, mix = None):
    """
    Executes a transfer from a transfer_dict dictionary that contains pipette and vol entries 
    """
    for transfer in transfer_dict:
        transfer_pipette = transfer['pipette']
        transfer_volume = transfer['vol']

        if mix is None:
            transfer_pipette.transfer(transfer_volume, source_well, sample_well, new_tip = 'always')
        else:
            transfer_pipette.transfer(transfer_volume, source_well, sample_well, new_tip = 'always', mix = mix)

        return None





    