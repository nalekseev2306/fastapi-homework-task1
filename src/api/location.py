from typing import List
from fastapi import APIRouter, status, Depends

from schemas.location import LocationResponse, LocationCreate
from domain.location.use_cases import *


router = APIRouter()


@router.get('/locations/', response_model=List[LocationResponse],
            status_code=status.HTTP_200_OK)
async def get_all_locations(
    use_case: GetLocationsUseCase = Depends()
) -> List[LocationResponse]:
    return await use_case.execute()


@router.get('/locations/{location_id}', response_model=LocationResponse,
            status_code=status.HTTP_200_OK)
async def get_location(
    location_id: int,
    use_case: GetLocationUseCase = Depends()
) -> LocationResponse:
    return await use_case.execute(location_id=location_id)


@router.get('/locations/by-name/{name}', response_model=LocationResponse,
            status_code=status.HTTP_200_OK)
async def get_location_by_locationname(
    name: str,
    use_case: GetLocationBySlugUseCase = Depends()
) -> LocationResponse:
    return await use_case.execute(name=name)


@router.post('/locations/', response_model=LocationResponse,
             status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    use_case: CreateLocationUseCase = Depends()
) -> LocationResponse:
    return await use_case.execute(location_data=location_data)


@router.delete('/locations/{location_id}', response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    use_case: DeleteLocationUseCase = Depends()
) -> None:
    return await use_case.execute(location_id=location_id)
