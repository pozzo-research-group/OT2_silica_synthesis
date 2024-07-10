

def prepare_silica_nanoparticles(P50, P300, stock_vials, sample_well, ethanol_vol, ammonia_vol, water_vol, TEOS_vol):
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

    ethanol_transfers = decide_pipette(P50, P300, ethanol_vol)
    ammonia_transfer = decide_pipette(P50, P300, ammonia_vol)
    water_transfer = decide_pipette(P50, P300, water_vol)
    TEOS_transfer = decide_pipette(P50, P300, TEOS_vol)
    # add water and TEOS 




    # execute ethanol transfers
    execute_transfer(P50, P300, ethanol_transfers, ethanol_stock, sample_well)
    execute_transfer(P50, P300, ammonia_transfer, ammonia_stock, sample_well)
    print('Starting water transfer, mix should be true')
    execute_transfer(P50, P300, water_transfer, water_stock, sample_well, mix_after = (15, 300))
    print('Starting TEOS transfer, mix should be true')
    execute_transfer(P50, P300, TEOS_transfer, TEOS_stock, sample_well, mix_after = (15, 300))

    return

def decide_pipette(P50, P300, volume):
    """
    Given a volume, decide if a P20 or P300 pipette should be used to transfer

    return: 'P50' or 'P300'
    """

    assert volume < 400, 'Volume must be less than 400 uL'

    if volume < 50:
        transfer = [{'pipette':P50, 'vol':volume}]
    
    elif volume > 50:
        # more complex logic to decide how to divide transfers 
        if volume < 300:
            transfer = [{'pipette':P300, 'vol':volume}]
        if volume > 300:
            transfer_vol = volume/2
            transfer = [{'pipette':P300, 'vol':transfer_vol}]*2

    
    return transfer

def execute_transfer(P50, P300, transfer_dict, source_well, sample_well, mix_after = None):
    """
    Executes a transfer from a transfer_dict dictionary that contains pipette and vol entries 
    """
    for transfer in transfer_dict:
        transfer_pipette = transfer['pipette']
        transfer_volume = transfer['vol']
        print('Executing transfer')
        print('Transfer pipette', transfer_pipette)
        print('Transfer volume :', transfer_volume)
        
        print('mix value :', mix_after)
        
        if mix_after is None:
            print('Mix is none, no mix executed')
            transfer_pipette.transfer(transfer_volume, source_well, sample_well, new_tip = 'always')
        else:
            print('Mix is true, should be mixing')
            #if using P300: execute transfer and mix with P300
            if transfer_pipette == P300:
                transfer_pipette.transfer(transfer_volume, source_well, sample_well, new_tip = 'always', mix_after = mix_after)
            
            # if using P50:
            elif transfer_pipette == P50:
            # Execute transfer with P50
                transfer_pipette.transfer(transfer_volume, source_well, sample_well, new_tip = 'always')
            # Mix with the P300
                P300.pick_up_tip()
                P300.mix(15,300,sample_well)
                P300.drop_tip()
        return None





    